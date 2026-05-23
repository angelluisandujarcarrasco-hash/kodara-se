"""
Añade meta tags de no-cache a TODOS los HTML del directorio kodara-se.
Esto fuerza al navegador a recargar siempre la última versión sin caché.
"""
import os

OUT_DIR = r"C:\Users\lucie\kodara-se"

NO_CACHE_TAGS = '''<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
'''

html_files = [f for f in os.listdir(OUT_DIR) if f.endswith(".html")]

count_ok = 0
count_skip = 0

for filename in sorted(html_files):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'no-cache, no-store' in content:
        count_skip += 1
        continue

    # Insertar después del <meta charset="UTF-8">
    if '<meta charset="UTF-8">' in content:
        content = content.replace(
            '<meta charset="UTF-8">',
            '<meta charset="UTF-8">\n' + NO_CACHE_TAGS.rstrip(),
            1
        )
    elif '<meta charset="utf-8">' in content:
        content = content.replace(
            '<meta charset="utf-8">',
            '<meta charset="utf-8">\n' + NO_CACHE_TAGS.rstrip(),
            1
        )
    else:
        # Fallback: insertar después de <head>
        content = content.replace(
            '<head>',
            '<head>\n' + NO_CACHE_TAGS.rstrip(),
            1
        )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    count_ok += 1

print(f"DONE — {count_ok} archivos actualizados, {count_skip} ya tenian no-cache")
