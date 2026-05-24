"""
Quita la nota visible al cliente sobre tamaños no disponibles + el optgroup deshabilitado.
Esa info era solo para configurar, no para mostrar.
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

files = [
    "pedido-colgadores-mate-premium.html",
    "pedido-colgadores-mate-clasico.html",
    "pedido-colgadores-mate-museo.html",
    "pedido-colgadores-semibrillante-premium.html",
    "pedido-colgadores-semibrillante-clasico.html",
]

# Patrón del optgroup deshabilitado
disabled_optgroup_re = re.compile(
    r'\s*<optgroup label="Tamaños NO disponibles para colgadores">\s*'
    r'<option disabled>13 × 18 cm — no disponible</option>\s*'
    r'<option disabled>15 × 20 cm — no disponible</option>\s*'
    r'</optgroup>\s*',
    re.DOTALL
)

# Patrón del step-sub que dice "Nota: 13×18..."
note_re = re.compile(
    r'\s*<strong style="color:#ff6b6b">Nota: 13×18 cm y 15×20 cm no disponibles para colgadores\.</strong>'
)

for filename in files:
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Quitar optgroup deshabilitado
    new_content, n1 = disabled_optgroup_re.subn('\n', content)
    # Quitar la nota roja
    new_content, n2 = note_re.subn('', new_content)

    if n1 > 0 or n2 > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"OK {filename}  (optgroup: {n1}, nota: {n2})")
    else:
        print(f"-- {filename}  sin cambios")

print("\nDONE")
