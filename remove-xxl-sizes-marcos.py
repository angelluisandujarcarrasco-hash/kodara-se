"""
Quita los 2 tamaños más grandes (75x100 cm y A0) del selector de tamaños
en todas las páginas de pedido de Marco de Madera, Prémium Madera y Marco de Metal.
Los marcos no llegan a esos tamaños tan grandes en Gelato.

También actualiza el step-sub con nuevo count (27) y nuevo precio máximo.
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

# Lista de archivos a modificar (13 en total)
files = [
    # Marco de Madera (5)
    "pedido-marco-madera-mate-premium.html",
    "pedido-marco-madera-mate-clasico.html",
    "pedido-marco-madera-mate-museo.html",
    "pedido-marco-madera-semibrillante-clasico.html",
    "pedido-marco-madera-semibrillante-premium.html",
    # Prémium Madera (3)
    "pedido-premium-madera-mate-premium.html",
    "pedido-premium-madera-mate-museo.html",
    "pedido-premium-madera-semibrillante-premium.html",
    # Marco de Metal (5)
    "pedido-marco-metal-mate-premium.html",
    "pedido-marco-metal-mate-clasico.html",
    "pedido-marco-metal-mate-museo.html",
    "pedido-marco-metal-semibrillante-premium.html",
    "pedido-marco-metal-semibrillante-clasico.html",
]

# Patrones para borrar las 2 últimas opciones
opt_75x100_re = re.compile(
    r'\s*<option data-price="\d+" value="75x100 cm[^"]*">[^<]*</option>\n?'
)
opt_a0_re = re.compile(
    r'\s*<option data-price="\d+" value="A0[^"]*">[^<]*</option>\n?'
)

# Regex para encontrar precios en options (para recalcular max)
price_re = re.compile(r'data-price="(\d+)"')

# Regex para step-sub
stepsub_re = re.compile(
    r'<p class="step-sub">El tamaño final[^<]+ Disponibles \d+ tamaños desde \$\d+ hasta \$\d+\.[^<]*</p>'
)

count_files = 0
for filename in files:
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename} (no existe)")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Quitar opciones de 75x100 cm y A0
    new_content, n1 = opt_75x100_re.subn("", content)
    new_content, n2 = opt_a0_re.subn("", new_content)

    if n1 == 0 and n2 == 0:
        print(f"SKIP {filename} (ya no tenían 75x100 o A0)")
        continue

    # Recalcular max y min de precios actuales
    prices = [int(m) for m in price_re.findall(new_content)]
    if not prices:
        print(f"FAIL {filename} (no se encontraron precios)")
        continue
    pmin = min(prices)
    pmax = max(prices)
    count_total = len(prices)

    # Reemplazar step-sub
    # Buscar el step-sub actual y reemplazarlo
    old_stepsub_match = stepsub_re.search(new_content)
    if old_stepsub_match:
        # Mantener el texto inicial pero actualizar tamaños y precio
        # Distinguir entre "póster con marco" y "póster"
        if "póster con marco prémium" in old_stepsub_match.group():
            tipo = "póster con marco prémium"
        elif "póster con marco" in old_stepsub_match.group():
            tipo = "póster con marco"
        else:
            tipo = "póster"
        new_stepsub = f'<p class="step-sub">El tamaño final del {tipo} que recibirás. Disponibles {count_total} tamaños desde ${pmin} hasta ${pmax}.</p>'
        new_content = stepsub_re.sub(new_stepsub, new_content, count=1)

    # También actualizar el label del optgroup XL si existe
    # El último optgroup probablemente sigue siendo "Tamaños XL · $X-$X" pero el rango cambió
    xl_optgroup_re = re.compile(r'<optgroup label="Tamaños XL · \$\d+–\$\d+">')
    xl_prices = []
    # Encontrar precios dentro del optgroup XL
    xl_block_re = re.compile(
        r'<optgroup label="Tamaños XL[^"]*">(.*?)</optgroup>',
        re.DOTALL
    )
    xl_match = xl_block_re.search(new_content)
    if xl_match:
        xl_prices = [int(m) for m in price_re.findall(xl_match.group(1))]
        if xl_prices:
            xl_min, xl_max = min(xl_prices), max(xl_prices)
            xl_label = f'<optgroup label="Tamaños XL · ${xl_min}–${xl_max}">'
            if xl_min == xl_max:
                xl_label = f'<optgroup label="Tamaños XL · ${xl_min}">'
            new_content = xl_optgroup_re.sub(xl_label, new_content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"OK {filename}  ({count_total} tamaños, rango ${pmin}-${pmax})")
    count_files += 1

print(f"\nDONE — {count_files}/13 archivos actualizados")
