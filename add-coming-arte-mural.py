"""
Marca como 'Próximamente' las 8 sub-categorías no listas de personalizar-arte-mural.html.
Listas: Impresión Artística, Pósteres, Marco de Madera, Prémium Madera
No listas: Marco de Metal, Con Colgadores, Lienzos, Lienzos Enmarcados, En Aluminio, En Plexiglás, En Espuma, En Madera
"""
import re
import os

OUT_DIR = r"C:\Users\lucie\kodara-se"
path = os.path.join(OUT_DIR, "personalizar-arte-mural.html")

# Productos NO listos (los href del botón Personalizar para identificarlos)
not_ready_hrefs = [
    "arte-mural-marco-metal.html",
    "arte-mural-colgadores.html",
    "arte-mural-lienzos.html",
    "arte-mural-lienzos-enmarcados.html",
    "arte-mural-aluminio.html",
    "arte-mural-plexiglas.html",
    "arte-mural-espuma.html",
    "arte-mural-madera.html",
]

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

count = 0
for href in not_ready_hrefs:
    # Para cada tarjeta no lista:
    # 1. Cambiar <article class="sub-card"> → <article class="sub-card coming">
    # 2. Añadir <span class="sub-card-soon">Próximamente</span> dentro de sub-card-img
    # 3. Cambiar el <a href="X.html" class="sub-card-cta">Elegir</a> por <span class="sub-card-cta-disabled">Próximamente</span>

    # Estrategia: buscamos el bloque article completo que contiene este href
    # Patrón: <article class="sub-card">.*?<a href="HREF" ...</a>.*?</article>

    pattern = re.compile(
        r'(<article class="sub-card">\s*<div class="sub-card-img">\s*)(<img class="img-base"[^>]*>\s*<img class="img-hover"[^>]*>\s*</div>\s*<div class="sub-card-body">\s*<h2 class="sub-card-title">[^<]+</h2>\s*)<a href="' + re.escape(href) + r'" class="sub-card-cta">[^<]+</a>',
        re.DOTALL
    )

    # Verificar que NO sea ya "coming"
    # Buscar la sección que rodea href
    idx = content.find(f'href="{href}"')
    if idx == -1:
        print(f"SKIP {href} (no encontrado)")
        continue
    # Mirar 600 chars atrás
    before = content[max(0,idx-600):idx]
    if 'sub-card coming' in before:
        print(f"SKIP {href} (ya tiene 'coming')")
        continue

    # Hacer reemplazo
    new_content, n = pattern.subn(
        r'<article class="sub-card coming">\n      <div class="sub-card-img">\n        <span class="sub-card-soon">Próximamente</span>\n        ' +
        r'\2'.replace("<article class=\"sub-card\">", "").replace('<div class="sub-card-img">\n        ', '') +
        r'<span class="sub-card-cta-disabled">Próximamente</span>',
        content,
        count=1
    )
    if n > 0:
        content = new_content
        count += 1
        print(f"OK {href}")
    else:
        # Patrón distinto, intentar más simple
        # Solo añadir 'coming' al article y cambiar el botón
        # Primero: buscar el article que contiene este href
        article_pattern = re.compile(
            r'<article class="sub-card">((?:(?!</article>).)*?<a href="' + re.escape(href) + r'" class="sub-card-cta">[^<]+</a>(?:(?!</article>).)*?)</article>',
            re.DOTALL
        )
        m = article_pattern.search(content)
        if m:
            inner = m.group(1)
            # Añadir <span class="sub-card-soon">Próximamente</span> después de <div class="sub-card-img">
            new_inner = inner.replace(
                '<div class="sub-card-img">\n',
                '<div class="sub-card-img">\n        <span class="sub-card-soon">Próximamente</span>\n',
                1
            )
            # Cambiar <a class="sub-card-cta">X</a> por <span class="sub-card-cta-disabled">Próximamente</span>
            new_inner = re.sub(
                r'<a href="' + re.escape(href) + r'" class="sub-card-cta">[^<]+</a>',
                '<span class="sub-card-cta-disabled">Próximamente</span>',
                new_inner
            )
            new_article = '<article class="sub-card coming">' + new_inner + '</article>'
            content = content[:m.start()] + new_article + content[m.end():]
            count += 1
            print(f"OK {href} (fallback)")
        else:
            print(f"FAIL {href}")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"\nDONE — {count}/8 tarjetas marcadas como Próximamente")
