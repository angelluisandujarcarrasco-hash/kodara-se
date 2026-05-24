"""
Limpia el codigo basura que quedo despues del refactor en pedido-*.html.
El bug: la regex no comio todo el form.addEventListener viejo,
quedaron lineas sueltas que rompen el JS con syntax error.
"""
import os
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"
pages = sorted([f for f in os.listdir(OUT_DIR) if f.startswith("pedido-") and f.endswith(".html")])

count_ok = 0
count_clean = 0

for filename in pages:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Patron a limpiar: justo despues de mi nuevo "}, 1200);\n});" del addToCart
    # quedan lineas tipo "return;\n  }\n  if(zone.classList..."

    # Estrategia: encontrar "addToCart(item);" hasta el primer "});" que cierre el bloque,
    # y luego eliminar TODO hasta el siguiente </script>

    # Mas seguro: buscar el patron exacto que vimos
    # despues de "}, 1200);" + linea con solo "});" debe seguir directo "</script>"
    # si hay codigo entre ", 1200);\n});" y "</script>", borrarlo

    pattern = r'(\}, 1200\);\s*\}\);)([^<]*?)(\s*</script>)'

    def cleanup(m):
        before = m.group(1)
        middle = m.group(2)
        after = m.group(3)
        # Si middle tiene contenido que no sea whitespace, es basura
        if middle.strip():
            return before + after
        return m.group(0)

    content = re.sub(pattern, cleanup, content, flags=re.DOTALL)

    # Tambien: eliminar el final "});" duplicado si existe pattern "});\s*});"
    # como cuando hay leftover de form.addEventListener closing

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"CLEAN {filename}")
        count_clean += 1
    else:
        print(f"OK    {filename}  (sin basura)")
        count_ok += 1

print(f"\n=== DONE ===")
print(f"Limpiadas: {count_clean}")
print(f"Sin basura: {count_ok}")
