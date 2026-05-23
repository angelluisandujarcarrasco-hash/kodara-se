import os

OUT_DIR = r"C:\Users\lucie\kodara-se"

products = [
    "mate-premium",
    "mate-clasico",
    "mate-museo",
    "impresion-artistica",
    "semibrillante-premium",
    "semibrillante-clasico",
]

# 1. En arte-mural-posteres.html: cambiar todos los href de sub-paginas a paginas de pedido
posteres_path = os.path.join(OUT_DIR, "arte-mural-posteres.html")
with open(posteres_path, "r", encoding="utf-8") as f:
    content = f.read()
changes_made = 0
for key in products:
    old = f'href="arte-mural-posteres-{key}.html"'
    new = f'href="pedido-posteres-{key}.html"'
    if old in content:
        content = content.replace(old, new)
        changes_made += 1
with open(posteres_path, "w", encoding="utf-8") as f:
    f.write(content)
print(f"OK arte-mural-posteres.html  ({changes_made} links cambiados)")

# 2. En cada pedido-posteres-XXX.html: cambiar el "Volver" para que apunte a arte-mural-posteres.html
for key in products:
    pedido_path = os.path.join(OUT_DIR, f"pedido-posteres-{key}.html")
    if not os.path.exists(pedido_path):
        print(f"SKIP {pedido_path} (no existe)")
        continue
    with open(pedido_path, "r", encoding="utf-8") as f:
        pcontent = f.read()
    old_href = f'href="arte-mural-posteres-{key}.html"'
    new_href = 'href="arte-mural-posteres.html"'
    pcontent = pcontent.replace(old_href, new_href)
    # Tambien cambiar el texto del boton "← Volver" para que diga "← Volver a Pósteres"
    pcontent = pcontent.replace(
        '<a href="arte-mural-posteres.html" class="topnav-back">← Volver</a>',
        '<a href="arte-mural-posteres.html" class="topnav-back">← Volver a Pósteres</a>'
    )
    with open(pedido_path, "w", encoding="utf-8") as f:
        f.write(pcontent)
    print(f"OK pedido-posteres-{key}.html  (volver ajustado)")

# 3. Borrar las 6 sub-paginas intermedias
for key in products:
    intermediate = os.path.join(OUT_DIR, f"arte-mural-posteres-{key}.html")
    if os.path.exists(intermediate):
        os.remove(intermediate)
        print(f"DEL arte-mural-posteres-{key}.html")
    else:
        print(f"SKIP arte-mural-posteres-{key}.html (no existe)")

print("\nDONE")
