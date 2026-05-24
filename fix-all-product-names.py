"""
Cambia TODOS los nombres de productos a los nombres COMPLETOS de Gelato.
Corrige nombres en:
- Catálogos (arte-mural-*.html)
- Páginas de pedido (pedido-*.html)
- personalizar-arte-mural.html
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

# ========== MAPEO COMPLETO ==========
# Cada par: (nombre_corto, nombre_completo_gelato)

name_changes = [
    # ===== PÓSTERES (6) =====
    ("Papel Mate Prémium", "Póster de papel mate prémium"),
    ("Papel Mate Clásico", "Póster de papel mate clásico"),
    ("Mate Calidad Museo", "Póster de papel mate calidad museo"),
    # "Impresión Artística" en Pósteres ya está bien si dice "Póster Impresión Artística"
    ("Semibrillante Prémium", "Póster de papel semibrillante prémium"),
    ("Semibrillante Clásico", "Póster de papel semibrillante clásico"),

    # ===== MARCO DE MADERA (5) =====
    ("Mate Prémium con Marco de Madera", "Póster de papel mate prémium con marco de madera"),
    ("Mate Clásico con Marco de Madera", "Póster de papel mate clásico con marco de madera"),
    ("Mate Calidad Museo con Marco de Madera", "Póster de papel mate calidad museo con marco de madera"),
    ("Semibrillante Prémium con Marco de Madera", "Póster de papel semibrillante prémium con marco de madera"),
    ("Semibrillante Clásico con Marco de Madera", "Póster de papel semibrillante clásico con marco de madera"),
]

# Archivos a procesar (todos los HTML que pueden tener estos nombres)
files_to_process = [
    # Catálogos principales
    "personalizar-arte-mural.html",
    "arte-mural-posteres.html",
    "arte-mural-marco-madera.html",
    "arte-mural-premium-madera.html",
    "arte-mural-impresion-artistica.html",
    # Páginas de pedido de Pósteres (6)
    "pedido-posteres-mate-premium.html",
    "pedido-posteres-mate-clasico.html",
    "pedido-posteres-mate-museo.html",
    "pedido-posteres-impresion-artistica.html",
    "pedido-posteres-semibrillante-premium.html",
    "pedido-posteres-semibrillante-clasico.html",
    # Páginas de pedido de Marco de Madera (5)
    "pedido-marco-madera-mate-premium.html",
    "pedido-marco-madera-mate-clasico.html",
    "pedido-marco-madera-mate-museo.html",
    "pedido-marco-madera-semibrillante-premium.html",
    "pedido-marco-madera-semibrillante-clasico.html",
]

# Cambios especiales en arte-mural-posteres.html: títulos cortos eran "Papel Mate Prémium"
# Pero arte-mural-marco-madera.html YA tiene "Mate Prémium con Marco de Madera"
# Hay que ordenar los reemplazos para que NO interfieran entre sí
# Reemplazar los más largos PRIMERO, luego los cortos

# Ordenar por longitud descendente (más largo primero)
name_changes_sorted = sorted(name_changes, key=lambda x: -len(x[0]))

total_changes = 0
for filename in files_to_process:
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename} (no existe)")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    file_changes = 0
    for old, new in name_changes_sorted:
        if old in content and new not in content[:content.find(old)]:
            # Verificar que no haya ya un cambio (evitar doble reemplazo)
            c_before = content.count(old)
            # Hacer reemplazo SOLO si old no es subcadena de otro nombre más largo
            # Como ya ordenamos por longitud DESC, los más largos ya fueron reemplazados
            content = content.replace(old, new)
            c_after = content.count(old)
            changes = c_before - c_after
            if changes > 0:
                file_changes += changes

    if file_changes > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"OK {filename}  ({file_changes} cambios)")
        total_changes += file_changes
    else:
        print(f"-- {filename}  (sin cambios)")

print(f"\nDONE — {total_changes} cambios totales")
