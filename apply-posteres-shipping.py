"""
Aplica precios CON ENVÍO INCLUIDO (margen 50% sobre costo + envío $5.69-$6.69)
a los 6 formularios de pedido de Pósteres + actualiza badges 'Desde $X' del catálogo.
"""
import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"

# Precios con envío incluido (29 valores por producto)
products = {
    "pedido-posteres-mate-premium.html": {
        "badge_key": "mate-premium",
        "card_text": "Papel Mate Prémium",
        "prices": [
            # Pequeños (envío ~$5.69): añadir ~$11.38 a precios sin envío
            23, 23, 24, 24, 24, 25,
            # Medianos (envío ~$5.80-$5.90): añadir ~$11.60-$11.80
            26, 26, 27, 28, 28, 29, 30, 31,
            # Grandes (envío ~$6.00-$6.20): añadir ~$12.00-$12.40
            32, 33, 34, 35, 36, 37, 38, 41,
            # XL (envío ~$6.40-$6.69): añadir ~$12.80-$13.38
            42, 43, 45, 46, 48, 50, 51,
        ],
    },
    "pedido-posteres-mate-clasico.html": {
        "badge_key": "mate-clasico",
        "card_text": "Papel Mate Clásico",
        "prices": [
            20, 20, 21, 21, 21, 22,
            23, 23, 24, 24, 24, 25, 25, 26,
            27, 28, 28, 29, 30, 30, 31, 32,
            33, 34, 35, 36, 38, 40, 42,
        ],
    },
    "pedido-posteres-mate-museo.html": {
        "badge_key": "mate-museo",
        "card_text": "Mate Calidad Museo",
        "prices": [
            26, 26, 27, 27, 27, 29,
            30, 30, 31, 33, 33, 34, 35, 36,
            38, 39, 40, 41, 43, 44, 45, 48,
            53, 55, 57, 58, 61, 64, 68,
        ],
    },
    "pedido-posteres-impresion-artistica.html": {
        "badge_key": "impresion-artistica",
        "card_text": "Impresión Artística",
        "prices": [
            28, 28, 29, 29, 29, 31,
            32, 33, 34, 36, 36, 37, 38, 39,
            40, 42, 43, 44, 46, 47, 48, 51,
            53, 54, 57, 58, 60, 62, 65,
        ],
    },
    "pedido-posteres-semibrillante-premium.html": {
        "badge_key": "semibrillante-premium",
        "card_text": "Semibrillante Prémium",
        "prices": [
            22, 22, 23, 23, 23, 24,
            24, 25, 25, 26, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 38,
            41, 42, 44, 45, 47, 48, 50,
        ],
    },
    "pedido-posteres-semibrillante-clasico.html": {
        "badge_key": "semibrillante-clasico",
        "card_text": "Semibrillante Clásico",
        "prices": [
            19, 19, 20, 20, 20, 21,
            22, 22, 23, 23, 23, 24, 24, 25,
            26, 27, 27, 28, 29, 30, 30, 32,
            34, 35, 37, 37, 39, 40, 41,
        ],
    },
}

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

# Actualizar cada pedido-XXX
for filename, info in products.items():
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    content = select_re.sub(build_select_html(info["prices"]), content, count=1)
    pmin, pmax = min(info["prices"]), max(info["prices"])
    new_stepsub = f'<p class="step-sub">El tamaño final del póster que recibirás. Disponibles 29 tamaños desde ${pmin} hasta ${pmax}.</p>'
    content = stepsub_re.sub(new_stepsub, content, count=1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {filename}  rango ${pmin}-${pmax}")

# Actualizar badges 'Desde $X' en arte-mural-posteres.html
catalogo_path = os.path.join(OUT_DIR, "arte-mural-posteres.html")
with open(catalogo_path, "r", encoding="utf-8") as f:
    cat = f.read()

# Mapeo nombre tarjeta → nuevo Desde $X
new_desdes = {
    "Papel Mate Prémium": min(products["pedido-posteres-mate-premium.html"]["prices"]),
    "Papel Mate Clásico": min(products["pedido-posteres-mate-clasico.html"]["prices"]),
    "Mate Calidad Museo": min(products["pedido-posteres-mate-museo.html"]["prices"]),
    "Impresión Artística": min(products["pedido-posteres-impresion-artistica.html"]["prices"]),
    "Semibrillante Prémium": min(products["pedido-posteres-semibrillante-premium.html"]["prices"]),
    "Semibrillante Clásico": min(products["pedido-posteres-semibrillante-clasico.html"]["prices"]),
}

# Para cada tarjeta, encontrar el badge actual y cambiarlo
# Patrón aproximado: <span class="sub-card-price">Desde $X</span>
# Necesito identificar QUÉ badge corresponde a QUÉ producto.
# Voy a usar el card_text como ancla: buscar el bloque que contiene el card_text y cambiar el Desde $X cercano.

for filename, info in products.items():
    card_text = info["card_text"]
    new_price = min(info["prices"])
    # Patrón: buscamos el span price ANTES del título del producto, en el mismo article
    # Estructura: <span class="sub-card-price">Desde $X</span>...<h2 class="sub-card-title">CARD_TEXT</h2>
    pattern = re.compile(
        r'(<span class="sub-card-price">Desde )\$(\d+)(</span>)([^<]*<img[^>]*>[^<]*<img[^>]*>[^<]*</div>[^<]*<div class="sub-card-body">[^<]*<h2 class="sub-card-title">' + re.escape(card_text) + ')',
        re.DOTALL
    )
    new_cat, n = pattern.subn(r'\1$' + str(new_price) + r'\3\4', cat)
    if n > 0:
        cat = new_cat
        print(f"  Badge {card_text}: ${new_price}")
    else:
        print(f"  ⚠ NO MATCH: {card_text}")

with open(catalogo_path, "w", encoding="utf-8") as f:
    f.write(cat)
print(f"OK arte-mural-posteres.html (badges Desde $X actualizados)")

print("\nDONE — 6 paginas de pedido + catálogo actualizados con envío incluido")
