"""
Anade cart.js a TODAS las paginas html que no son pedido/carrito/checkout.
Para que el FAB del carrito sea visible en todo el sitio.
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

# Excluidas (ya tienen cart.js o no aplica)
EXCLUDE = set()  # ninguna por ahora

# Procesar TODOS los .html en la raiz
all_html = sorted([f for f in os.listdir(OUT_DIR) if f.endswith(".html") and not f.startswith(".")])
print(f"Procesando {len(all_html)} archivos HTML")

count_added = 0
count_skip = 0

for filename in all_html:
    if filename in EXCLUDE:
        continue
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'cart.js' in content:
        count_skip += 1
        continue

    if '</body>' not in content:
        print(f"WARN {filename}  (no </body>)")
        continue

    # Anadir antes de </body>
    new_content = content.replace('</body>', '<script src="cart.js"></script>\n</body>', 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"ADD  {filename}")
    count_added += 1

print(f"\n=== DONE ===")
print(f"Agregados: {count_added}")
print(f"Skip:      {count_skip}")
