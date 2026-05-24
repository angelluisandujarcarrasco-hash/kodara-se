"""
Cambia los nombres de Marco de Metal a los nombres COMPLETOS de Gelato:
- Categoría: 'Marco de Metal' → 'Pósteres con marco de metal'
- Productos: 'Mate Prémium con Marco de Metal' → 'Póster de papel mate prémium con marco de metal'
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

# Mapeo de nombres viejos → nuevos
name_map = {
    # Productos individuales (5)
    "Mate Prémium con Marco de Metal": "Póster de papel mate prémium con marco de metal",
    "Mate Clásico con Marco de Metal": "Póster de papel mate clásico con marco de metal",
    "Mate Calidad Museo con Marco de Metal": "Póster de papel mate calidad museo con marco de metal",
    "Semibrillante Prémium con Marco de Metal": "Póster de papel semibrillante prémium con marco de metal",
    "Semibrillante Clásico con Marco de Metal": "Póster de papel semibrillante clásico con marco de metal",
}

# Title de página: 'marco de metal' (gradient lowercase) se mantiene
# Page-tag: 'Arte Mural · Marco de Metal' → 'Arte Mural · Pósteres con marco de metal'
# Topnav back: '← Volver a Marco de Metal' → '← Volver a Pósteres con marco de metal'

archivos_a_modificar = [
    "arte-mural-marco-metal.html",
    "pedido-marco-metal-mate-premium.html",
    "pedido-marco-metal-mate-clasico.html",
    "pedido-marco-metal-mate-museo.html",
    "pedido-marco-metal-semibrillante-premium.html",
    "pedido-marco-metal-semibrillante-clasico.html",
    "personalizar-arte-mural.html",
]

total_changes = 0
for filename in archivos_a_modificar:
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename} (no existe)")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    file_changes = 0

    # Reemplazar nombres de productos
    for old, new in name_map.items():
        if old in content:
            c = content.count(old)
            content = content.replace(old, new)
            file_changes += c

    # Reemplazar categoría
    # En personalizar-arte-mural.html: <h2 class="sub-card-title">Marco de Metal</h2>
    if 'sub-card-title">Marco de Metal</h2>' in content:
        content = content.replace(
            '<h2 class="sub-card-title">Marco de Metal</h2>',
            '<h2 class="sub-card-title">Pósteres con marco de metal</h2>'
        )
        file_changes += 1

    # Page-tag en arte-mural-marco-metal.html
    content = content.replace(
        '<div class="page-tag">Arte Mural · Marco de Metal</div>',
        '<div class="page-tag">Arte Mural · Pósteres con marco de metal</div>'
    )

    # Page-tag en páginas de pedido: '<div class="page-tag">Pedido · Marco de Metal'
    # Pero no debería existir así, los pedidos tienen 'Pedido · NOMBRE_PRODUCTO'
    # Aún así verificamos

    # Topnav back: '← Volver a Marco de Metal'
    if '← Volver a Marco de Metal' in content:
        content = content.replace(
            '← Volver a Marco de Metal',
            '← Volver a Pósteres con marco de metal'
        )
        file_changes += 1

    # Title de página
    if '<title>Marco de Metal · Kodara Print Studio</title>' in content:
        content = content.replace(
            '<title>Marco de Metal · Kodara Print Studio</title>',
            '<title>Pósteres con marco de metal · Kodara Print Studio</title>'
        )

    # En arte-mural-marco-metal.html el title grande dice 'Personaliza tu marco de metal'
    # Cambiar a 'Personaliza tu póster con marco de metal'
    if 'Personaliza tu <span class="grad">marco de metal</span>' in content:
        content = content.replace(
            'Personaliza tu <span class="grad">marco de metal</span>',
            'Personaliza tu <span class="grad">póster con marco de metal</span>'
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK {filename}  ({file_changes} cambios)")
    total_changes += file_changes

print(f"\nDONE — {total_changes} cambios totales en {len(archivos_a_modificar)} archivos")
