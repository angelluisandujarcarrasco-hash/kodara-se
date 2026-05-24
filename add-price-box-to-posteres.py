"""
Anade el price-box display + JS update a los 6 pedido-posteres-*.html
que no lo tienen. Asi todos tienen consistencia visual y captura de precio.
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

# CSS a agregar (despues de .size-select rules)
NEW_CSS = """.price-box{display:flex;align-items:center;justify-content:space-between;gap:14px;background:linear-gradient(135deg, rgba(249,115,22,0.08), rgba(236,72,153,0.08));border:1px solid rgba(249,115,22,0.25);border-radius:14px;padding:18px 22px;margin-top:14px;transition:all 0.3s ease}
.price-box.active{border-color:var(--orange);background:linear-gradient(135deg, rgba(249,115,22,0.15), rgba(236,72,153,0.12))}
.price-label{font-size:12px;color:var(--text-3);font-weight:700;letter-spacing:1px;text-transform:uppercase}
.price-amount{font-size:clamp(28px,4vw,36px);font-weight:900;font-family:'JetBrains Mono',monospace;background:linear-gradient(135deg, var(--orange), var(--pink));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;line-height:1}
.price-amount.empty{background:none;-webkit-text-fill-color:var(--text-3);color:var(--text-3);font-size:18px;font-weight:600}"""

# HTML del price-box
PRICE_BOX_HTML = """
    <!-- Visualizador del precio -->
    <div class="price-box" id="price-box">
      <div class="price-label">Precio del póster</div>
      <div class="price-amount empty" id="price-amount">Elige un tamaño</div>
    </div>
    <input type="hidden" name="precio" id="precio-hidden" value="">"""

# JS del price-display (inyectar antes del ADD TO CART)
PRICE_JS = """
// ===== PRICE DISPLAY =====
const sizeSelectPB = document.getElementById('size-select');
const priceBox = document.getElementById('price-box');
const priceAmount = document.getElementById('price-amount');
const precioHiddenField = document.getElementById('precio-hidden');
if (sizeSelectPB) {
  sizeSelectPB.addEventListener('change', () => {
    const opt = sizeSelectPB.options[sizeSelectPB.selectedIndex];
    const price = opt.dataset.price;
    if (price) {
      priceAmount.textContent = '$' + price;
      priceAmount.classList.remove('empty');
      priceBox.classList.add('active');
      if (precioHiddenField) precioHiddenField.value = '$' + price;
    } else {
      priceAmount.textContent = 'Elige un tamaño';
      priceAmount.classList.add('empty');
      priceBox.classList.remove('active');
      if (precioHiddenField) precioHiddenField.value = '';
    }
  });
}
"""

# Target solo los 6 posteres que no tienen price-box
TARGETS = [
    "pedido-posteres-impresion-artistica.html",
    "pedido-posteres-mate-clasico.html",
    "pedido-posteres-mate-museo.html",
    "pedido-posteres-mate-premium.html",
    "pedido-posteres-semibrillante-clasico.html",
    "pedido-posteres-semibrillante-premium.html",
]

for filename in TARGETS:
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"MISSING {filename}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'id="price-box"' in content:
        print(f"SKIP    {filename}  (ya tiene)")
        continue

    # 1. Agregar CSS antes de </style>
    if '.size-select option' in content:
        # Insertar despues de .size-select option rule
        content = re.sub(
            r'(\.size-select option\{[^}]+\})',
            r'\1\n' + NEW_CSS,
            content,
            count=1
        )

    # 2. Agregar HTML del price-box despues del </select>
    # Buscar el </select> y luego el cierre del form-step
    pattern = r'(</select>)\s*\n(\s*</div>\s*\n\s*<!--)'
    content = re.sub(pattern, r'\1' + PRICE_BOX_HTML + r'\n\2', content, count=1)

    # 3. Agregar JS antes del comentario "// ===== ADD TO CART"
    content = content.replace(
        '// ===== ADD TO CART (reemplaza submit de Web3Forms) =====',
        PRICE_JS + '\n// ===== ADD TO CART (reemplaza submit de Web3Forms) ====='
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK      {filename}")

print("\nDONE")
