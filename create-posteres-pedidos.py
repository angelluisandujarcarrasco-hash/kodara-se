import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"
TEMPLATE_PATH = os.path.join(OUT_DIR, "pedido-impresion-artistica.html")

# Mapeo: clave-corta, sub-pagina, pedido-pagina, full-name, short-name, lowercase-name, img-base, img-hover
products = [
    ("mate-premium",
     "arte-mural-posteres-mate-premium.html",
     "pedido-posteres-mate-premium.html",
     "Papel Mate Prémium",
     "Mate Premium",
     "papel mate prémium",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162841_bc6f0ab7-a698-41fa-b8e0-6d54dc166845.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162857_02fbcbf9-dac0-46cf-8239-8e46f9f4e631.png"),
    ("mate-clasico",
     "arte-mural-posteres-mate-clasico.html",
     "pedido-posteres-mate-clasico.html",
     "Papel Mate Clásico",
     "Mate Clasico",
     "papel mate clásico",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162843_f5469e4b-25cc-4ae3-a536-c89a930ddcb8.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162900_ee19a234-26d1-463a-8226-f4b970685552.png"),
    ("mate-museo",
     "arte-mural-posteres-mate-museo.html",
     "pedido-posteres-mate-museo.html",
     "Mate Calidad Museo",
     "Mate Calidad Museo",
     "mate calidad museo",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162846_04b13009-a6fa-4dcc-8d64-74cd14f0da23.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162903_c2e57ba5-6b9f-4205-972b-7e16a00d9207.png"),
    ("impresion-artistica",
     "arte-mural-posteres-impresion-artistica.html",
     "pedido-posteres-impresion-artistica.html",
     "Impresión Artística (Póster)",
     "Impresion Artistica",
     "impresión artística",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162849_cf7a039c-78fc-4a3d-88a7-453f69ae9d75.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162905_968268db-6669-4cae-a14f-bb0eb5149e64.png"),
    ("semibrillante-premium",
     "arte-mural-posteres-semibrillante-premium.html",
     "pedido-posteres-semibrillante-premium.html",
     "Semibrillante Prémium",
     "Semibrillante Premium",
     "semibrillante prémium",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162852_e5e6fa3c-8dcd-42ad-886c-9f4be965c748.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162908_fe45160b-705c-470d-97bc-b74e3f95fe3a.png"),
    ("semibrillante-clasico",
     "arte-mural-posteres-semibrillante-clasico.html",
     "pedido-posteres-semibrillante-clasico.html",
     "Semibrillante Clásico",
     "Semibrillante Clasico",
     "semibrillante clásico",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162854_e05eda28-e65b-4f4c-a908-ab50208ee302.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_162911_edfb8fee-45c3-4ece-80ed-a1edfe6efe5b.png"),
]

# ========== PARTE 1: Crear 6 páginas de pedido basadas en pedido-impresion-artistica.html ==========
with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
    template = f.read()

for key, subpage, pedido, full, short, lower, _base, _hover in products:
    new_html = template
    # Title
    new_html = new_html.replace(
        "<title>Hacer mi pedido · Impresión Artística · Kodara Print</title>",
        f"<title>Hacer mi pedido · {full} · Kodara Print</title>"
    )
    # Topnav back links (logo + back button) → apuntan a la sub-página correspondiente
    new_html = new_html.replace(
        'href="arte-mural-impresion-artistica.html"',
        f'href="{subpage}"'
    )
    # Page tag chip
    new_html = new_html.replace(
        '<div class="page-tag">Pedido · Impresión Artística</div>',
        f'<div class="page-tag">Pedido · {full}</div>'
    )
    # Web3Forms subject
    new_html = new_html.replace(
        'value="Nuevo pedido · Impresión Artística · Kodara Print"',
        f'value="Nuevo pedido · {full} · Kodara Print"'
    )
    out = os.path.join(OUT_DIR, pedido)
    with open(out, "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"OK PEDIDO  {pedido}")

# ========== PARTE 2: Reescribir las 6 sub-páginas con tarjeta de pedido ==========
subpage_template = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{full_name} · Kodara Print Studio</title>
<link rel="icon" type="image/jpeg" href="logo-kodara.jpeg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#060B18;--bg-2:#0A1424;--card:#0F1A2E;--card-2:#131F36;--border:rgba(255,255,255,0.06);--border-2:rgba(255,255,255,0.1);--text:#fff;--text-2:#B8C0D0;--text-3:#6B7689;--orange:#F97316;--orange-light:#FB923C;--pink:#EC4899;--purple:#7C3AED;--yellow:#F59E0B}}
*{{margin:0;padding:0;box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden;min-height:100vh}}
::selection{{background:var(--orange);color:#fff}}
a{{color:inherit;text-decoration:none}}
img{{max-width:100%;display:block}}
.topnav{{position:sticky;top:0;z-index:100;background:rgba(6,11,24,0.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:14px 32px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}}
.topnav-logo{{display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px}}
.topnav-logo img{{width:36px;height:36px;border-radius:8px}}
.topnav-logo span{{color:var(--orange);font-size:12px;font-weight:600}}
.topnav-back{{background:transparent;border:1px solid var(--border-2);color:var(--text-2);font-size:13px;padding:8px 16px;border-radius:999px;font-weight:600;transition:all 0.2s}}
.topnav-back:hover{{border-color:var(--orange);color:var(--orange)}}
.page-header{{position:relative;padding:80px 32px 60px;text-align:center;background:radial-gradient(ellipse at top, rgba(124,58,237,0.12), transparent 60%),radial-gradient(ellipse at bottom, rgba(249,115,22,0.08), transparent 60%),var(--bg);border-bottom:1px solid var(--border)}}
.page-header::before{{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);background-size:64px 64px;mask:radial-gradient(ellipse at center, black 30%, transparent 70%);-webkit-mask:radial-gradient(ellipse at center, black 30%, transparent 70%);pointer-events:none}}
.page-header-inner{{position:relative;z-index:2;max-width:800px;margin:0 auto}}
.page-tag{{display:inline-flex;align-items:center;gap:8px;background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.3);color:var(--orange);font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;padding:8px 16px;border-radius:999px;letter-spacing:1px;margin-bottom:20px;text-transform:uppercase}}
.page-tag::before{{content:'';width:6px;height:6px;border-radius:50%;background:var(--orange);box-shadow:0 0 12px var(--orange)}}
.page-title{{font-size:clamp(32px,5vw,56px);font-weight:900;letter-spacing:-1.5px;line-height:1.12;margin-bottom:18px}}
.page-title .grad{{background:linear-gradient(135deg, var(--orange), var(--pink), var(--purple));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;display:inline-block;padding-bottom:0.08em}}
.page-sub{{font-size:clamp(15px,1.6vw,18px);color:var(--text-2);max-width:560px;margin:0 auto;line-height:1.55}}
.main-content{{max-width:1100px;margin:0 auto;padding:60px 32px 100px;min-height:40vh}}
.sub-services{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,260px));gap:18px;justify-content:center}}
.sub-card{{background:var(--card);border:1px solid var(--border);border-radius:18px;overflow:hidden;transition:all 0.3s ease;display:flex;flex-direction:column}}
.sub-card:hover{{transform:translateY(-4px);border-color:var(--orange);box-shadow:0 12px 36px rgba(249,115,22,0.15)}}
.sub-card-img{{position:relative;aspect-ratio:1/1;overflow:hidden;background:var(--bg-2)}}
.sub-card-img img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity 0.45s ease, transform 0.6s ease}}
.sub-card-img .img-base{{opacity:1;z-index:1}}
.sub-card-img .img-hover{{opacity:0;z-index:2}}
.sub-card:hover .img-base{{opacity:0}}
.sub-card:hover .img-hover{{opacity:1;transform:scale(1.04)}}
.sub-card-body{{padding:16px;display:flex;flex-direction:column;gap:12px}}
.sub-card-title{{font-size:16px;font-weight:800;letter-spacing:-0.3px;line-height:1.2;text-align:center}}
.sub-card-cta{{display:inline-flex;align-items:center;justify-content:center;gap:6px;background:linear-gradient(135deg, var(--orange), var(--pink));color:#fff;font-size:13px;font-weight:700;padding:11px 18px;border-radius:999px;transition:all 0.25s}}
.sub-card-cta:hover{{transform:translateY(-2px);box-shadow:0 8px 24px rgba(249,115,22,0.3)}}
.sub-card-cta::after{{content:'→';font-size:14px}}
.footer{{border-top:1px solid var(--border);padding:32px;text-align:center;color:var(--text-3);font-size:13px}}
.footer a{{color:var(--orange)}}
@media(max-width:640px){{.topnav{{padding:12px 18px}}.page-header{{padding:60px 20px 40px}}.main-content{{padding:40px 20px 60px}}}}
</style>
</head>
<body>

<nav class="topnav">
  <a href="arte-mural-posteres.html" class="topnav-logo">
    <img src="logo-kodara.jpeg" alt="Kodara SE">
    <div>Kodara <span>PRINT</span></div>
  </a>
  <a href="arte-mural-posteres.html" class="topnav-back">← Volver a Pósteres</a>
</nav>

<header class="page-header">
  <div class="page-header-inner">
    <div class="page-tag">Pósteres · {short_name}</div>
    <h1 class="page-title">
      Personaliza tu <span class="grad">{lower_name}</span>.
    </h1>
    <p class="page-sub">
      Configura tu pedido en un solo paso: tamaño, orientación, tu imagen y nos lo envías.
    </p>
  </div>
</header>

<main class="main-content">
  <div class="sub-services">

    <article class="sub-card">
      <div class="sub-card-img">
        <img class="img-base" src="{img_base}" alt="{full_name}">
        <img class="img-hover" src="{img_hover}" alt="{full_name} en pared">
      </div>
      <div class="sub-card-body">
        <h2 class="sub-card-title">{full_name}</h2>
        <a href="{pedido_page}" class="sub-card-cta">Personalizar</a>
      </div>
    </article>

  </div>
</main>

<footer class="footer">
  © 2026 Kodara SE · <a href="index.html">kodarase.com</a>
</footer>

</body>
</html>
'''

for key, subpage, pedido, full, short, lower, base, hover in products:
    content = subpage_template.format(
        full_name=full,
        short_name=short,
        lower_name=lower,
        img_base=base,
        img_hover=hover,
        pedido_page=pedido,
    )
    out_path = os.path.join(OUT_DIR, subpage)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"OK SUBPAGE {subpage}")

print("\nDONE - 6 pedido pages + 6 sub-pages updated")
