"""
Actualiza pedido-impresion-artistica.html:
1. Nuevos precios con envío incluido ($28-$65 en lugar de $17-$51)
2. Añade aviso 'Envío gratis a todo el mundo' arriba del selector
3. Actualiza step-sub con nuevo rango
También actualiza el badge 'Desde $X' en arte-mural-impresion-artistica.html
"""
import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"

# 29 precios nuevos (envío incluido + margen 50%)
prices = [
    # Pequeños
    28, 28, 29, 29, 29, 31,
    # Medianos
    32, 33, 34, 36, 36, 37, 38, 39,
    # Grandes
    40, 42, 43, 44, 46, 47, 48, 51,
    # XL
    53, 54, 57, 58, 60, 62, 65,
]

size_defs = [
    ('13x18 cm / 5x7"', '13 × 18 cm  ·  5 × 7"', 'pequenos'),
    ('15x20 cm / 6x8"', '15 × 20 cm  ·  6 × 8"', 'pequenos'),
    ('20x25 cm / 8x10"', '20 × 25 cm  ·  8 × 10"', 'pequenos'),
    ('21x29.7 cm / A4', '21 × 29.7 cm  ·  A4', 'pequenos'),
    ('25x25 cm / 10x10"', '25 × 25 cm  ·  10 × 10"  (cuadrado)', 'pequenos'),
    ('20x50 cm / 8x20"', '20 × 50 cm  ·  8 × 20"  (panorámico)', 'pequenos'),
    ('25x60 cm / 10x24"', '25 × 60 cm  ·  10 × 24"  (panorámico)', 'medianos'),
    ('27x35 cm / 11x14"', '27 × 35 cm  ·  11 × 14"', 'medianos'),
    ('28x43 cm / XL 11x17"', '28 × 43 cm  ·  XL 11 × 17"', 'medianos'),
    ('A3 / 29.7x42 cm', 'A3  ·  29.7 × 42 cm', 'medianos'),
    ('30x30 cm / 12x12"', '30 × 30 cm  ·  12 × 12"  (cuadrado)', 'medianos'),
    ('30x40 cm / 12x16"', '30 × 40 cm  ·  12 × 16"', 'medianos'),
    ('30x45 cm / 12x18"', '30 × 45 cm  ·  12 × 18"', 'medianos'),
    ('35x35 cm / 14x14"', '35 × 35 cm  ·  14 × 14"  (cuadrado)', 'medianos'),
    ('40x40 cm / 16x16"', '40 × 40 cm  ·  16 × 16"  (cuadrado)', 'grandes'),
    ('40x50 cm / 16x20"', '40 × 50 cm  ·  16 × 20"', 'grandes'),
    ('40x60 cm / 16x24"', '40 × 60 cm  ·  16 × 24"', 'grandes'),
    ('A2 / 42x59.4 cm', 'A2  ·  42 × 59.4 cm', 'grandes'),
    ('45x45 cm / 18x18"', '45 × 45 cm  ·  18 × 18"  (cuadrado)', 'grandes'),
    ('45x60 cm / 18x24"', '45 × 60 cm  ·  18 × 24"', 'grandes'),
    ('50x50 cm / 20x20"', '50 × 50 cm  ·  20 × 20"  (cuadrado)', 'grandes'),
    ('50x70 cm / 20x28"', '50 × 70 cm  ·  20 × 28"', 'grandes'),
    ('A1 / 59.4x84.1 cm', 'A1  ·  59.4 × 84.1 cm', 'xl'),
    ('60x80 cm / 24x32"', '60 × 80 cm  ·  24 × 32"', 'xl'),
    ('60x90 cm / 24x36"', '60 × 90 cm  ·  24 × 36"', 'xl'),
    ('70x70 cm / 28x28"', '70 × 70 cm  ·  28 × 28"  (cuadrado)', 'xl'),
    ('70x100 cm / 28x40"', '70 × 100 cm  ·  28 × 40"', 'xl'),
    ('75x100 cm / 30x40"', '75 × 100 cm  ·  30 × 40"', 'xl'),
    ('A0 / 84.1x118.9 cm', 'A0  ·  84.1 × 118.9 cm  (XXL)', 'xl'),
]

def build_select_html():
    grupos = {'pequenos': [], 'medianos': [], 'grandes': [], 'xl': []}
    for (sv, sl, g), p in zip(size_defs, prices):
        grupos[g].append((sv, sl, p))

    def fmt_value(sv, p): return f'{sv} · ${p}'.replace('"', '&quot;')
    def fmt_label(sl, p): return f'{sl}  —  ${p}'

    def render_group(label, items):
        gmin = min(p for _, _, p in items)
        gmax = max(p for _, _, p in items)
        rango = f'${gmin}' if gmin == gmax else f'${gmin}–${gmax}'
        opts = []
        for sv, sl, p in items:
            opts.append(f'        <option data-price="{p}" value="{fmt_value(sv, p)}">{fmt_label(sl, p)}</option>')
        return f'      <optgroup label="{label} · {rango}">\n' + '\n'.join(opts) + '\n      </optgroup>'

    out = '    <select class="size-select" name="tamano" id="size-select" required>\n'
    out += '      <option value="" disabled selected>— Selecciona un tamaño —</option>\n\n'
    out += render_group("Tamaños pequeños", grupos['pequenos']) + '\n\n'
    out += render_group("Tamaños medianos", grupos['medianos']) + '\n\n'
    out += render_group("Tamaños grandes", grupos['grandes']) + '\n\n'
    out += render_group("Tamaños XL", grupos['xl']) + '\n'
    out += '    </select>'
    return out


# ========== 1. pedido-impresion-artistica.html ==========
path = os.path.join(OUT_DIR, "pedido-impresion-artistica.html")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Reemplazar el bloque <select>
select_re = re.compile(r'<select class="size-select"[^>]*>.*?</select>', re.DOTALL)
content = select_re.sub(build_select_html(), content, count=1)

# Reemplazar el step-sub con nuevo rango y mensaje "Envío gratis"
stepsub_re = re.compile(r'<p class="step-sub">El tamaño final[^<]*</p>')
new_stepsub = f'<p class="step-sub">El tamaño final del póster que recibirás. <strong style="color:#10B981">🚚 Envío gratis a todo el mundo incluido.</strong> Disponibles 29 tamaños desde ${min(prices)} hasta ${max(prices)}.</p>'
content = stepsub_re.sub(new_stepsub, content, count=1)

# Añadir badge "Envío gratis" visible debajo del precio (después del </div> que cierra .price-box)
# Buscamos: <div class="price-amount empty" id="price-amount">Elige un tamaño</div>\n    </div>
shipping_badge = '''
    <div class="shipping-badge">
      <span class="shipping-icon">🚚</span>
      <strong>Envío gratis</strong> · a todo el mundo · ya incluido en el precio
    </div>'''

# Insertar después de </div> de .price-box (que termina la price-amount + </div>)
content = content.replace(
    '<div class="price-amount empty" id="price-amount">Elige un tamaño</div>\n    </div>',
    '<div class="price-amount empty" id="price-amount">Elige un tamaño</div>\n    </div>' + shipping_badge
)

# Añadir CSS para .shipping-badge
shipping_css = '''
.shipping-badge{
  display:flex;align-items:center;justify-content:center;gap:8px;
  background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);
  border-radius:12px;padding:12px 18px;margin-top:12px;
  font-size:13px;color:#10B981;font-weight:600;text-align:center;
}
.shipping-badge strong{color:#10B981;font-weight:800}
.shipping-icon{font-size:18px}
'''

# Insertar antes de "/* price display */"
content = content.replace(
    '/* price display */',
    shipping_css + '\n/* price display */'
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"OK pedido-impresion-artistica.html — rango ${min(prices)}–${max(prices)} + Envío gratis")


# ========== 2. arte-mural-impresion-artistica.html (badge "Desde $28") ==========
path2 = os.path.join(OUT_DIR, "arte-mural-impresion-artistica.html")
with open(path2, "r", encoding="utf-8") as f:
    c2 = f.read()
c2 = c2.replace(
    '<span class="sub-card-price">Desde $17</span>',
    f'<span class="sub-card-price">Desde ${min(prices)}</span>'
)
with open(path2, "w", encoding="utf-8") as f:
    f.write(c2)
print(f"OK arte-mural-impresion-artistica.html — badge Desde ${min(prices)}")

print("\nDONE")
