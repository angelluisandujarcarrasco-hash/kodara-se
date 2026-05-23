"""
Añade el botón '← Volver a Kodara' en el topnav de todas las páginas demo y
cambia el href del logo de https://kodarase.com a index.html (link relativo interno).
"""
import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"

demo_files = [
    "demo-marketing.html",
    "demo-auditoria-seo.html",
    "demo-auditoria-meta-ads.html",
    "demo-auditoria-negocio.html",
    "demo-automatizaciones.html",
    "demo-prospeccion.html",
    "demo-chat-ia.html",
    "demo-dashboard-facturas.html",
    "demo-instagram-web.html",
    "clinica-norte.html",
]

# CSS del botón Volver
css_back = """.topnav-back{background:transparent;border:1px solid rgba(255,255,255,0.12);color:#B8C0D0;font-size:13px;padding:8px 16px;border-radius:999px;font-weight:600;transition:all 0.2s;text-decoration:none;white-space:nowrap}
.topnav-back:hover{border-color:#F97316;color:#F97316}
"""

# Botón Volver a Kodara
back_btn_html = '<a href="index.html" class="topnav-back">← Volver a Kodara</a>'

for filename in demo_files:
    path = os.path.join(OUT_DIR, filename)
    if not os.path.exists(path):
        print(f"SKIP {filename}")
        continue

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'class="topnav-back"' in content:
        print(f"SKIP {filename} (ya tiene botón Volver)")
        continue

    # 1. Cambiar el href del logo de "https://kodarase.com" a "index.html"
    content = content.replace(
        'href="https://kodarase.com" class="topnav-logo"',
        'href="index.html" class="topnav-logo"'
    )

    # 2. Insertar CSS .topnav-back si no está (antes del último </style>)
    if '.topnav-back{' not in content:
        content = content.replace('</style>', css_back + '</style>', 1)

    # 3. Insertar el botón Volver después del </a> del topnav-logo
    # Patrón: el logo termina con </a> y le sigue un <div... (el grupo derecho)
    # Voy a buscar el cierre del </a> del logo y meter el botón antes del siguiente elemento
    # El logo tiene structure: <a href="..." class="topnav-logo"...>...</a>
    # Después viene: <div style="display:flex;align-items:center;gap:12px">

    # Busco </a>\n  <div style="display:flex (el grupo derecho)
    # Lo reemplazo por </a>\n  <a href...volver><\a>\n  <div style="display:flex
    pattern = re.compile(
        r'(</a>)(\s*<div style="display:flex;align-items:center;gap:12px")',
    )
    new_content, n = pattern.subn(
        r'\1\n  ' + back_btn_html + r'\2',
        content,
        count=1,
    )

    if n > 0:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"OK   {filename}")
    else:
        # Fallback: encontrar el final del </a> del topnav-logo y agregar después
        pattern2 = re.compile(
            r'(class="topnav-logo"[^>]*>.*?</a>)',
            re.DOTALL
        )
        new_content, n = pattern2.subn(
            r'\1\n  ' + back_btn_html,
            content,
            count=1,
        )
        if n > 0:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"OK   {filename} (fallback)")
        else:
            print(f"FAIL {filename}")

print("\nDONE")
