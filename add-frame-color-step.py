"""
Añade el paso 'Color del marco' a las 5 paginas pedido-marco-madera-XXX.html.
Renumera los pasos siguientes (imagen 3→4, datos 4→5).
Añade validación JS del color del marco.
"""
import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"

files = [
    "pedido-marco-madera-mate-premium.html",
    "pedido-marco-madera-mate-clasico.html",
    "pedido-marco-madera-semibrillante-clasico.html",
    "pedido-marco-madera-semibrillante-premium.html",
    "pedido-marco-madera-mate-museo.html",
]

# CSS a insertar antes de /* form fields */
new_css = '''/* color del marco */
.frame-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.frame-opt{cursor:pointer;background:var(--bg-2);border:2px solid var(--border-2);border-radius:14px;padding:18px 10px;text-align:center;transition:all 0.2s;display:flex;flex-direction:column;align-items:center;gap:10px}
.frame-opt:hover{border-color:var(--orange-light)}
.frame-opt input{display:none}
.frame-opt:has(input:checked){border-color:var(--orange);background:rgba(249,115,22,0.08)}
.frame-swatch{width:52px;height:52px;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.35)}
.frame-label{font-weight:700;font-size:12px;line-height:1.2}

'''

# HTML del nuevo paso 3 (color del marco)
new_step_html = '''  <!-- 3 · COLOR DEL MARCO -->
  <div class="form-step">
    <div class="step-head">
      <div class="step-num">3</div>
      <div class="step-title">Color del marco</div>
    </div>
    <p class="step-sub">Elige el color del marco de madera que prefieras.</p>
    <div class="frame-grid">
      <label class="frame-opt">
        <input type="radio" name="color_marco" value="Blanco" required>
        <div class="frame-swatch" style="background:#FAFAFA;border:1px solid #DDD"></div>
        <div class="frame-label">Blanco</div>
      </label>
      <label class="frame-opt">
        <input type="radio" name="color_marco" value="Madera natural">
        <div class="frame-swatch" style="background:linear-gradient(135deg, #D4A977 0%, #B5854F 100%)"></div>
        <div class="frame-label">Madera natural</div>
      </label>
      <label class="frame-opt">
        <input type="radio" name="color_marco" value="Madera oscura">
        <div class="frame-swatch" style="background:linear-gradient(135deg, #6B4423 0%, #3D2814 100%)"></div>
        <div class="frame-label">Madera oscura</div>
      </label>
      <label class="frame-opt">
        <input type="radio" name="color_marco" value="Negro">
        <div class="frame-swatch" style="background:#1a1a1a;border:1px solid #333"></div>
        <div class="frame-label">Negro</div>
      </label>
    </div>
  </div>

'''

# Validación JS a insertar después de la del paso 2 (orientación)
new_validation_js = '''    // 3. Validar color del marco
    const colorMarco = form.querySelector('[name="color_marco"]:checked');
    if (!colorMarco) {
      e.preventDefault();
      showAlert('Tienes que elegir el color del marco (paso 3).');
      return;
    }
'''

# Media query addition (frame-grid 2 columnas en móvil)
mq_addition = '  .frame-grid{grid-template-columns:1fr 1fr}\n  '

for filename in files:
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # ---- 1. Insertar CSS del color del marco antes de /* form fields */ ----
    content = content.replace(
        "/* form fields */",
        new_css + "/* form fields */",
        1
    )

    # ---- 2. Insertar nuevo paso 3 (color del marco) antes del paso actual 3 (imagen) ----
    # El paso 3 actual empieza con "<!-- 3 · IMAGEN"
    content = content.replace(
        '  <!-- 3 · IMAGEN (subida directa a Cloudinary) -->',
        new_step_html + '  <!-- 4 · IMAGEN (subida directa a Cloudinary) -->'
    )

    # ---- 3. Renumerar step-num: 3→4 (imagen) ----
    # Encontrar el paso de imagen y cambiar su step-num de 3 a 4
    content = content.replace(
        '<!-- 4 · IMAGEN (subida directa a Cloudinary) -->\n  <div class="form-step">\n    <div class="step-head">\n      <div class="step-num">3</div>\n      <div class="step-title">Tu imagen</div>',
        '<!-- 4 · IMAGEN (subida directa a Cloudinary) -->\n  <div class="form-step">\n    <div class="step-head">\n      <div class="step-num">4</div>\n      <div class="step-title">Tu imagen</div>'
    )

    # ---- 4. Renumerar step-num: 4→5 (datos de envío) ----
    content = content.replace(
        '<!-- 4 · TUS DATOS DE ENVÍO -->\n  <div class="form-step">\n    <div class="step-head">\n      <div class="step-num">4</div>',
        '<!-- 5 · TUS DATOS DE ENVÍO -->\n  <div class="form-step">\n    <div class="step-head">\n      <div class="step-num">5</div>'
    )

    # ---- 5. Insertar validación JS del color del marco antes de la validación #3 (imagen) ----
    # La validación de imagen empieza con "// 3. Validar imagen subida a Cloudinary"
    content = content.replace(
        '    // 3. Validar imagen subida a Cloudinary',
        new_validation_js + '    // 4. Validar imagen subida a Cloudinary'
    )
    # Renumerar comentarios siguientes:
    content = content.replace(
        '    // 4. Validar que la zona no esté en estado de subida',
        '    // 5. Validar que la zona no esté en estado de subida'
    )

    # ---- 6. Media query: añadir frame-grid 2 columnas en móvil ----
    content = content.replace(
        '  .size-grid{grid-template-columns:1fr 1fr}\n',
        '  .size-grid{grid-template-columns:1fr 1fr}\n' + mq_addition
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {filename}")

print("\nDONE - paso 'Color del marco' añadido a las 5 paginas")
