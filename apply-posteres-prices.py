"""
Aplica precios margen 50% a los formularios de pedido de Pósteres.
Reescribe el bloque <select class="size-select"> con los precios correctos para cada producto.
"""
import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"

# Cada producto: (filename, [29 precios en orden])
products = {
    "pedido-posteres-mate-premium.html": [
        # Pequeños
        11, 11, 12, 12, 12, 13,
        # Medianos
        14, 14, 15, 16, 16, 17, 18, 19,
        # Grandes
        20, 21, 22, 23, 24, 25, 26, 28,
        # XL
        29, 30, 32, 33, 35, 37, 38,
    ],
    "pedido-posteres-mate-clasico.html": [
        9, 9, 10, 10, 10, 10,
        11, 11, 12, 12, 12, 13, 13, 14,
        15, 16, 16, 17, 18, 18, 19, 20,
        21, 22, 23, 24, 25, 27, 29,
    ],
    "pedido-posteres-mate-museo.html": [
        15, 15, 16, 16, 16, 17,
        18, 18, 19, 21, 21, 22, 23, 24,
        26, 27, 28, 29, 31, 32, 33, 35,
        40, 42, 44, 45, 48, 51, 55,
    ],
    "pedido-posteres-impresion-artistica.html": [
        # Mismo que la categoría principal: $17–$51
        17, 17, 18, 18, 18, 19,
        20, 21, 22, 24, 24, 25, 26, 27,
        28, 30, 31, 32, 34, 35, 36, 38,
        40, 41, 44, 45, 47, 49, 51,
    ],
    "pedido-posteres-semibrillante-premium.html": [
        10, 11, 11, 11, 11, 12,
        12, 13, 13, 14, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 23, 24, 26,
        28, 29, 31, 32, 34, 35, 36,
    ],
    "pedido-posteres-semibrillante-clasico.html": [
        8, 8, 9, 9, 9, 9,
        10, 10, 11, 11, 11, 12, 12, 13,
        14, 15, 15, 16, 17, 18, 18, 20,
        21, 22, 24, 24, 26, 27, 28,
    ],
}

# Estructura de cada tamaño en orden
size_defs = [
    # (size_value, size_label, group)
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
    """Genera el HTML del <select> completo con los precios dados."""
    # Calcular rangos por grupo
    grupos = {'pequenos': [], 'medianos': [], 'grandes': [], 'xl': []}
    for (size_value, size_label, group), price in zip(size_defs, prices):
        grupos[group].append((size_value, size_label, price))

    def fmt_value(sv, p):
        return f'{sv} · ${p}'.replace('"', '&quot;')
    def fmt_label(sl, p):
        return f'{sl}  —  ${p}'

    def render_group(label, items):
        prices_in = [p for _, _, p in items]
        gmin, gmax = min(prices_in), max(prices_in)
        rango = f'${gmin}' if gmin == gmax else f'${gmin}–${gmax}'
        options = []
        for sv, sl, p in items:
            options.append(f'        <option data-price="{p}" value="{fmt_value(sv, p)}">{fmt_label(sl, p)}</option>')
        opts_str = '\n'.join(options)
        return f'      <optgroup label="{label} · {rango}">\n{opts_str}\n      </optgroup>'

    out = '''    <select class="size-select" name="tamano" id="size-select" required>
      <option value="" disabled selected>— Selecciona un tamaño —</option>

'''
    out += render_group("Tamaños pequeños", grupos['pequenos']) + '\n\n'
    out += render_group("Tamaños medianos", grupos['medianos']) + '\n\n'
    out += render_group("Tamaños grandes", grupos['grandes']) + '\n\n'
    out += render_group("Tamaños XL", grupos['xl']) + '\n'
    out += '    </select>'
    return out


# regex que captura el bloque <select ...> ... </select>
select_re = re.compile(r'<select class="size-select"[^>]*>.*?</select>', re.DOTALL)
# regex para el step-sub que dice "29 tamaños"
stepsub_re = re.compile(r'<p class="step-sub">El tamaño final[^<]*</p>')

for filename, prices in products.items():
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename} (no existe)")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_select = build_select_html(prices)
    new_content, n = select_re.subn(new_select, content, count=1)

    pmin, pmax = min(prices), max(prices)
    new_stepsub = f'<p class="step-sub">El tamaño final del póster que recibirás. Disponibles 29 tamaños — desde ${pmin} hasta ${pmax}.</p>'
    new_content, n2 = stepsub_re.subn(new_stepsub, new_content, count=1)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK {filename}  ({n} select, {n2} step-sub) — rango ${pmin}–${pmax}")

print("\nDONE - 6 pedido pages updated with margin 50% prices")
