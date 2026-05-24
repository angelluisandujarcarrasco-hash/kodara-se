"""
Cambia los nombres de las 12 sub-categorías de Arte Mural a los nombres COMPLETOS de Gelato.
Aplica en personalizar-arte-mural.html y en cada catálogo + sus páginas de pedido.
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

# Mapeo de nombres cortos → nombres completos Gelato
# Ordenar por longitud DESC para evitar conflictos
category_map = [
    ("Pósteres prémium enmarcados en madera", "Pósteres prémium enmarcados en madera"),  # ya OK
    ("Pósteres con marcos de madera", "Pósteres con marcos de madera"),
    ("Pósteres con marco de metal", "Pósteres con marco de metal"),  # ya OK
    ("Pósteres con colgadores", "Pósteres con colgadores"),
    ("Impresión en plexiglás", "Impresión en plexiglás"),  # ya OK
    ("Impresión en aluminio", "Impresión en aluminio"),  # ya OK
    ("Impresiones en madera", "Impresiones en madera"),  # ya OK
    ("Lienzos enmarcados", "Lienzos enmarcados"),
    ("Impresión en espuma", "Impresión en espuma"),  # ya OK
    ("Impresión Artística", "Impresión Artística"),  # ya OK
    ("Marco de Madera", "Pósteres con marcos de madera"),
    ("Prémium Madera", "Pósteres prémium enmarcados en madera"),
    ("Con Colgadores", "Pósteres con colgadores"),
    ("En Aluminio", "Impresión en aluminio"),
    ("En Plexiglás", "Impresión en plexiglás"),
    ("En Espuma", "Impresión en espuma"),
    ("En Madera", "Impresiones en madera"),
    ("Lienzos Enmarcados", "Lienzos enmarcados"),
]

# Ordenar por longitud del "viejo" DESC para reemplazar primero los más largos
category_map_sorted = sorted(category_map, key=lambda x: -len(x[0]))

# Solo proceso personalizar-arte-mural.html donde están las 12 tarjetas
# Los catálogos individuales ya tienen sus propios nombres (los corregidos)
files_to_process = [
    "personalizar-arte-mural.html",
]

# Cambios específicos del page-tag/title/back-button de los catálogos:
# Ya están corregidos en marco-metal. Hay que corregir los demás también.

# Mapeo de cambios específicos (textos que cambian en HTML)
specific_changes = {
    # arte-mural-marco-madera.html
    "arte-mural-marco-madera.html": [
        ("<div class=\"page-tag\">Arte Mural · Marco de Madera</div>",
         "<div class=\"page-tag\">Arte Mural · Pósteres con marcos de madera</div>"),
    ],
    # arte-mural-premium-madera.html
    "arte-mural-premium-madera.html": [
        ("<div class=\"page-tag\">Arte Mural · Marco Madera Prémium</div>",
         "<div class=\"page-tag\">Arte Mural · Pósteres prémium enmarcados en madera</div>"),
    ],
    # pedido-marco-madera-*.html → cambiar "Volver a Marco de Madera"
    "pedido-marco-madera-mate-premium.html": [
        ("← Volver a Marco de Madera", "← Volver a Pósteres con marcos de madera"),
    ],
    "pedido-marco-madera-mate-clasico.html": [
        ("← Volver a Marco de Madera", "← Volver a Pósteres con marcos de madera"),
    ],
    "pedido-marco-madera-mate-museo.html": [
        ("← Volver a Marco de Madera", "← Volver a Pósteres con marcos de madera"),
    ],
    "pedido-marco-madera-semibrillante-premium.html": [
        ("← Volver a Marco de Madera", "← Volver a Pósteres con marcos de madera"),
    ],
    "pedido-marco-madera-semibrillante-clasico.html": [
        ("← Volver a Marco de Madera", "← Volver a Pósteres con marcos de madera"),
    ],
    "pedido-premium-madera-mate-premium.html": [
        ("← Volver a Marco Prémium", "← Volver a Pósteres prémium enmarcados en madera"),
    ],
    "pedido-premium-madera-mate-museo.html": [
        ("← Volver a Marco Prémium", "← Volver a Pósteres prémium enmarcados en madera"),
    ],
    "pedido-premium-madera-semibrillante-premium.html": [
        ("← Volver a Marco Prémium", "← Volver a Pósteres prémium enmarcados en madera"),
    ],
}

# ===== APLICAR CAMBIOS =====

total = 0

# 1. personalizar-arte-mural.html con los 12 nombres de tarjetas
path = os.path.join(OUT_DIR, "personalizar-arte-mural.html")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

file_changes = 0
for old, new in category_map_sorted:
    if old == new:
        continue
    # Solo reemplazar dentro del título de tarjeta
    old_html = f'<h2 class="sub-card-title">{old}</h2>'
    new_html = f'<h2 class="sub-card-title">{new}</h2>'
    if old_html in content:
        c = content.count(old_html)
        content = content.replace(old_html, new_html)
        file_changes += c

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"OK personalizar-arte-mural.html  ({file_changes} cambios)")
total += file_changes

# 2. Cambios específicos en otros archivos
for filename, changes in specific_changes.items():
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    file_changes = 0
    for old, new in changes:
        if old in content:
            c = content.count(old)
            content = content.replace(old, new)
            file_changes += c
    if file_changes > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"OK {filename}  ({file_changes} cambios)")
        total += file_changes

print(f"\nDONE — {total} cambios totales")
