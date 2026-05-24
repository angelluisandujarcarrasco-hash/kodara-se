"""
Restaura el optgroup 'No disponibles' en el selector de colgadores.
Pone solo 'No disponibles' como label, con las 2 opciones desactivadas.
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

# Bloque a insertar (después de la option default "-- Selecciona un tamaño --")
new_optgroup = '''
      <optgroup label="No disponibles">
        <option disabled>13 × 18 cm</option>
        <option disabled>15 × 20 cm</option>
      </optgroup>
'''

for filename in files:
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename}")
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verificar que no tenga ya el optgroup
    if '<optgroup label="No disponibles">' in content:
        print(f"SKIP {filename}  (ya tiene optgroup)")
        continue

    # Insertar después de la option "-- Selecciona un tamaño --"
    pattern = r'(<option value="" disabled selected>— Selecciona un tamaño —</option>\n)'
    new_content, n = re.subn(pattern, r'\1' + new_optgroup, content, count=1)

    if n > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"OK {filename}")
    else:
        print(f"FAIL {filename}  (no se encontró patrón)")

print("\nDONE")
