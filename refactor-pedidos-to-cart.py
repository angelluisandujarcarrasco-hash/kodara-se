"""
Refactoriza todas las paginas pedido-*.html para usar el carrito.
Cambios:
1. Anade <script src="cart.js"></script> antes de </body>
2. Quita el form de Web3Forms (action, hidden fields)
3. Quita el ultimo form-step (Datos de envio)
4. Cambia "Enviar pedido" -> "Agregar al carrito"
5. Modifica el JS para guardar al carrito en lugar de enviar a Web3Forms
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

# Listar paginas pedido
pages = sorted([f for f in os.listdir(OUT_DIR) if f.startswith("pedido-") and f.endswith(".html")])
print(f"Encontradas {len(pages)} paginas pedido")

# JS nuevo que reemplaza la logica de submit
NEW_SUBMIT_JS = '''
// ===== ADD TO CART (reemplaza submit de Web3Forms) =====
function getProductName() {
  // Obtiene el nombre del producto desde el subject hidden o el page-tag
  const subj = document.querySelector('input[name="subject"]');
  if (subj && subj.value) {
    return subj.value.replace('Nuevo pedido · ', '').replace(' · Kodara Print', '').trim();
  }
  const tag = document.querySelector('.page-tag');
  if (tag) return tag.textContent.replace('Pedido · ', '').trim();
  return 'Producto Kodara Print';
}

const form = document.querySelector('form.form-wrap');
const alertBox = document.getElementById('form-alert');
const submitBtn = document.getElementById('submit-btn');

function showAlert(msg){
  if (!alertBox) { alert(msg); return; }
  alertBox.textContent = '⚠ ' + msg;
  alertBox.classList.add('show');
  alertBox.scrollIntoView({behavior:'smooth',block:'center'});
  setTimeout(()=>alertBox.classList.remove('show'), 6000);
}

form.addEventListener('submit', (e) => {
  e.preventDefault();

  // Validar selecciones obligatorias
  const radiosByName = {};
  form.querySelectorAll('input[type="radio"][required]').forEach(r => {
    if (!radiosByName[r.name]) radiosByName[r.name] = r.checked;
    else radiosByName[r.name] = radiosByName[r.name] || r.checked;
  });
  for (const [name, checked] of Object.entries(radiosByName)) {
    const anyChecked = form.querySelector(`input[name="${name}"]:checked`);
    if (!anyChecked) {
      showAlert(`Elige una opción de ${name.replace('_', ' ')}.`);
      return;
    }
  }

  // Validar select de tamano
  const tamano = form.querySelector('[name="tamano"]');
  if (tamano && !tamano.value) {
    showAlert('Tienes que elegir un tamaño.');
    tamano.focus();
    return;
  }

  // Validar imagen
  const urlField = form.querySelector('#imagen-url');
  if (urlField && (!urlField.value || !urlField.value.startsWith('https://res.cloudinary.com/'))) {
    showAlert('Tienes que subir una imagen.');
    const zone = document.getElementById('upload-zone');
    if (zone) zone.scrollIntoView({behavior:'smooth', block:'center'});
    return;
  }

  // Validar que no esta subiendo aun
  const zone = document.getElementById('upload-zone');
  if (zone && zone.classList.contains('uploading')) {
    showAlert('Espera a que termine de subirse la imagen.');
    return;
  }

  // Construir item del carrito
  const item = {
    producto: getProductName(),
    pedido_page: window.location.pathname.split('/').pop()
  };

  // Capturar todos los radios checked
  form.querySelectorAll('input[type="radio"]:checked').forEach(r => {
    item[r.name] = r.value;
  });

  // Capturar select
  if (tamano && tamano.value) item.tamano = tamano.value;

  // Capturar precio del precio-hidden o del data-price del option
  const precioHidden = form.querySelector('#precio-hidden');
  if (precioHidden && precioHidden.value) {
    item.precio_str = precioHidden.value;
    const match = precioHidden.value.match(/\\$(\\d+)/);
    if (match) item.precio_num = parseInt(match[1]);
  }

  // Capturar imagen
  if (urlField) item.imagen_url = urlField.value;

  // Capturar notas si existen
  const notas = form.querySelector('[name="notas"]');
  if (notas && notas.value.trim()) item.notas_producto = notas.value.trim();

  // Agregar al carrito
  if (!item.precio_num) {
    showAlert('No se pudo determinar el precio. Selecciona un tamaño.');
    return;
  }

  addToCart(item);
  showCartToast('¡Agregado al carrito!', 'Ver carrito →', 'carrito.html');

  // Resetear form para permitir agregar otro
  setTimeout(() => {
    if (confirm('¿Agregar otro producto similar o ir al carrito?\\n\\nOK = Ir al carrito\\nCancelar = Seguir agregando')) {
      window.location.href = 'carrito.html';
    } else {
      // Reset solo imagen y notas, mantener seleccion
      if (urlField) urlField.value = '';
      const previewImg = document.getElementById('upload-preview');
      const uploadIcon = document.getElementById('upload-icon');
      const uploadText = document.getElementById('upload-text');
      const uploadHint = document.getElementById('upload-hint');
      const status = document.getElementById('upload-status');
      const clearBtn = document.getElementById('upload-clear');
      if (zone) zone.classList.remove('done', 'uploading');
      if (uploadIcon) { uploadIcon.style.display = ''; uploadIcon.textContent = '📁'; }
      if (uploadText) { uploadText.style.display = ''; uploadText.textContent = 'Arrastra tu imagen aquí o haz clic para elegirla'; }
      if (uploadHint) uploadHint.style.display = '';
      if (previewImg) { previewImg.style.display = 'none'; previewImg.src = ''; }
      if (status) status.textContent = '';
      if (clearBtn) clearBtn.style.display = 'none';
      const fileInput = document.getElementById('file-input');
      if (fileInput) fileInput.value = '';
      window.scrollTo({top: 0, behavior: 'smooth'});
    }
  }, 1200);
});
'''

count_ok = 0
count_skip = 0

for filename in pages:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Skip si ya tiene cart.js
    if 'cart.js' in content and 'addToCart(item)' in content:
        print(f"SKIP {filename} (ya tiene carrito)")
        count_skip += 1
        continue

    # 1. Quitar el step "Datos de envio" (form-step que contiene "datos de envío")
    # Busca el div.form-step que contiene "Tus datos de envío" o "Datos de envío"
    pattern = r'<!--\s*\d+\s*·\s*(?:TUS\s+)?DATOS\s+DE\s+ENVÍO\s*-->.*?(?=<div\s+class="form-alert"|<button\s+type="submit")'
    content_new = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)

    # Tambien quitar comentarios alternativos
    if content_new == content:
        pattern2 = r'<div\s+class="form-step">\s*<div\s+class="step-head">\s*<div\s+class="step-num">\d+</div>\s*<div\s+class="step-title">(?:Tus\s+)?[Dd]atos\s+de\s+env[ií]o</div>.*?</div>\s*(?=<div\s+class="form-alert"|<button\s+type="submit")'
        content_new = re.sub(pattern2, '', content, flags=re.DOTALL)

    content = content_new

    # 2. Cambiar texto del boton submit a "Agregar al carrito"
    content = re.sub(
        r'(<button\s+type="submit"[^>]*>)(Enviar\s+pedido)(</button>)',
        r'\1Agregar al carrito\3',
        content,
        flags=re.IGNORECASE
    )

    # 3. Modificar el ::after del .submit-btn (lo cambia de '→' a '🛒+' o ya esta bien con flecha)
    # Mantener flecha pero podemos cambiar a 🛒. Mejor mantener flecha.

    # 4. Reemplazar el handler form.addEventListener('submit', ...) con NEW_SUBMIT_JS
    # Busca el bloque del form.addEventListener
    # El patron es: const form = document.querySelector('form.form-wrap');
    # hasta el cierre de form.addEventListener('submit', ...)
    submit_pattern = r"//\s*===+\s*FORM\s+(?:SUBMIT\s+)?VALIDATION\s*===+.*?form\.addEventListener\('submit',.*?\}\);?\s*"
    content = re.sub(submit_pattern, lambda m: NEW_SUBMIT_JS, content, flags=re.DOTALL | re.IGNORECASE)

    # Variante sin comentario header
    if 'addToCart(item)' not in content:
        # buscar form.addEventListener directamente
        submit_pattern2 = r"const\s+form\s*=\s*document\.querySelector\('form\.form-wrap'\);.*?form\.addEventListener\('submit',.*?\}\);?\s*"
        content = re.sub(submit_pattern2, lambda m: NEW_SUBMIT_JS, content, flags=re.DOTALL)

    # 5. Anadir cart.js antes de </body> si no esta
    if 'cart.js' not in content:
        content = content.replace('</body>', '<script src="cart.js"></script>\n</body>', 1)

    # 6. Quitar/inhabilitar el action de Web3Forms (form action y hidden fields)
    # Mantenemos el action para que si alguien fuerza submit no rompa, pero el JS lo intercepta
    # Mejor cambiar action a "#"
    content = re.sub(
        r'(<form\s+class="form-wrap"\s+)action="https://api\.web3forms\.com/submit"\s+method="POST"',
        r'\1action="#" method="POST" novalidate',
        content
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    if 'addToCart(item)' in content:
        print(f"OK   {filename}")
        count_ok += 1
    else:
        print(f"WARN {filename}  (cart.js anadido pero JS submit no detectado para reemplazar)")

print(f"\n=== DONE ===")
print(f"OK:   {count_ok}")
print(f"SKIP: {count_skip}")
print(f"Total: {len(pages)}")
