"""
Aplica precios CON ENVÍO INCLUIDO (margen 50%) a los 3 formularios de Marco Madera Prémium.
También actualiza badges 'Desde $X' del catálogo arte-mural-premium-madera.html
"""
import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"

products = [
    {
        "key": "mate-premium",
        "card_text": "Póster con marco de madera prémium con papel mate prémium",
        "costo_min": 27.44, "costo_max": 134.02,
    },
    {
        "key": "mate-museo",
        "card_text": "Póster con marco de madera prémium con papel mate de calidad museo",
        "costo_min": 32.15, "costo_max": 145.03,
    },
    {
        "key": "semibrillante-premium",
        "card_text": "Póster con marco de madera prémium con papel semibrillante prémium",
        "costo_min": 27.00, "costo_max": 133.22,
    },
]

ENVIO_MIN = 12.99
ENVIO_MAX = 36.99

posiciones = [
    0.00, 0.02, 0.05, 0.05, 0.05, 0.08,
    0.12, 0.13, 0.16, 0.20, 0.20, 0.24, 0.28, 0.32,
    0.37, 0.42, 0.47, 0.50, 0.55, 0.59, 0.62, 0.68,
    0.74, 0.78, 0.84, 0.87, 0.92, 0.96, 1.00,
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

def calc_prices(costo_min, costo_max):
    prices = []
    for pos in posiciones:
        costo_prod = costo_min + pos * (costo_max - costo_min)
        envio = ENVIO_MIN + pos * (ENVIO_MAX - ENVIO_MIN)
        precio = round((costo_prod + envio) * 2)
        prices.append(precio)
    return prices

def build_select_html(prices):
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

select_re = re.compile(r'<select class="size-select"[^>]*>.*?</select>', re.DOTALL)
stepsub_re = re.compile(r'<p class="step-sub">El tamaño final[^<]*</p>')

catalogo_path = os.path.join(OUT_DIR, "arte-mural-premium-madera.html")
with open(catalogo_path, "r", encoding="utf-8") as f:
    cat = f.read()

# Asegurar CSS .sub-card-price
if '.sub-card-price{' not in cat:
    css_badge = ".sub-card-price{position:absolute;top:10px;right:10px;background:linear-gradient(135deg, var(--orange), var(--pink));color:#fff;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:800;padding:6px 12px;border-radius:999px;letter-spacing:0.3px;z-index:3;box-shadow:0 4px 16px rgba(249,115,22,0.35)}\n"
    cat = cat.replace(
        ".sub-card-cta::after{content:'→';font-size:14px}\n",
        ".sub-card-cta::after{content:'→';font-size:14px}\n" + css_badge
    )

for prod in products:
    prices = calc_prices(prod["costo_min"], prod["costo_max"])
    filename = f"pedido-premium-madera-{prod['key']}.html"
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = select_re.sub(build_select_html(prices), content, count=1)
    pmin, pmax = min(prices), max(prices)
    new_stepsub = f'<p class="step-sub">El tamaño final del póster con marco prémium que recibirás. Disponibles 29 tamaños desde ${pmin} hasta ${pmax}.</p>'
    content = stepsub_re.sub(new_stepsub, content, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {filename}  rango ${pmin}-${pmax}")

    # Añadir badge 'Desde $X' al catálogo
    card_text = prod["card_text"]
    article_pattern = re.compile(
        r'(<article class="sub-card">\s*<div class="sub-card-img">\s*)(<img class="img-base"[^>]*>\s*<img class="img-hover"[^>]*>\s*</div>\s*<div class="sub-card-body">\s*<h2 class="sub-card-title">' + re.escape(card_text) + r'</h2>)',
        re.DOTALL
    )
    new_badge = f'<span class="sub-card-price">Desde ${pmin}</span>\n        '
    # Verificar si ya tiene badge
    card_idx = cat.find(card_text)
    if card_idx != -1 and 'sub-card-price' not in cat[max(0, card_idx-500):card_idx]:
        cat, n = article_pattern.subn(r'\1' + new_badge + r'\2', cat)
        if n > 0:
            print(f"  Badge añadido: Desde ${pmin}")

with open(catalogo_path, "w", encoding="utf-8") as f:
    f.write(cat)
print("OK arte-mural-premium-madera.html (badges actualizados)")

print("\nDONE — 3 paginas de pedido + catálogo Premium Madera con precios margen 50%")
