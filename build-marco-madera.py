"""
Construye:
1. arte-mural-marco-madera.html con las 5 tarjetas (doble imagen + link directo a pedido)
2. 5 paginas pedido-marco-madera-XXX.html (basadas en pedido-impresion-artistica.html)
"""
import os
import re

OUT_DIR = r"C:\Users\lucie\kodara-se"

# Productos: (key, full_name, short_name, lower_name, base_img, hover_img, costo_min, precio_desde)
# Costo min de captura Gelato (con Gelato+). Margen 50% → precio = costo * 2.
products = [
    ("mate-premium",
     "Mate Prémium con Marco de Madera",
     "Mate Premium",
     "mate prémium con marco",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173623_ecdc26ce-5f58-4944-b3c7-f92cecf0ded3.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173637_8b2fe361-2af8-4cfd-ba4b-c63577bd99f2.png",
     14.88, 30),
    ("mate-clasico",
     "Mate Clásico con Marco de Madera",
     "Mate Clasico",
     "mate clásico con marco",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173626_52290e5f-be2e-402f-a30a-8fbd94e28f40.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173639_b1282466-2572-4cd2-a343-7af36ffc4568.png",
     13.34, 27),
    ("semibrillante-clasico",
     "Semibrillante Clásico con Marco de Madera",
     "Semibrillante Clasico",
     "semibrillante clásico con marco",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173628_578ae54f-231b-4c8b-8da3-25718bd8cd36.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173642_0584a7f0-5919-49fa-8502-e5f43fd0c576.png",
     12.85, 26),
    ("semibrillante-premium",
     "Semibrillante Prémium con Marco de Madera",
     "Semibrillante Premium",
     "semibrillante prémium con marco",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173631_88ecd388-317b-4539-8ffd-f9f4225b3c9d.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173645_542cd892-2488-4513-b7fb-aca1756afcdd.png",
     14.54, 29),
    ("mate-museo",
     "Mate Calidad Museo con Marco de Madera",
     "Mate Museo",
     "mate calidad museo con marco",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173634_e899b6bd-480a-4ee4-ac41-4c802da0d887.png",
     "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_173648_f05dcbea-d156-46f7-b338-5dd9157d005f.png",
     18.65, 37),
]

# ========== 1. CATÁLOGO arte-mural-marco-madera.html ==========
catalogo = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Marco de Madera · Kodara Print Studio</title>
<link rel="icon" type="image/jpeg" href="logo-kodara.jpeg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#060B18;--bg-2:#0A1424;--card:#0F1A2E;--card-2:#131F36;--border:rgba(255,255,255,0.06);--border-2:rgba(255,255,255,0.1);--text:#fff;--text-2:#B8C0D0;--text-3:#6B7689;--orange:#F97316;--orange-light:#FB923C;--pink:#EC4899;--purple:#7C3AED;--yellow:#F59E0B}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden;min-height:100vh}
::selection{background:var(--orange);color:#fff}
a{color:inherit;text-decoration:none}
img{max-width:100%;display:block}
.topnav{position:sticky;top:0;z-index:100;background:rgba(6,11,24,0.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:14px 32px;display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.topnav-logo{display:flex;align-items:center;gap:10px;font-weight:800;font-size:18px}
.topnav-logo img{width:36px;height:36px;border-radius:8px}
.topnav-logo span{color:var(--orange);font-size:12px;font-weight:600}
.topnav-back{background:transparent;border:1px solid var(--border-2);color:var(--text-2);font-size:13px;padding:8px 16px;border-radius:999px;font-weight:600;transition:all 0.2s}
.topnav-back:hover{border-color:var(--orange);color:var(--orange)}
.page-header{position:relative;padding:80px 32px 60px;text-align:center;background:radial-gradient(ellipse at top, rgba(124,58,237,0.12), transparent 60%),radial-gradient(ellipse at bottom, rgba(249,115,22,0.08), transparent 60%),var(--bg);border-bottom:1px solid var(--border)}
.page-header::before{content:'';position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);background-size:64px 64px;mask:radial-gradient(ellipse at center, black 30%, transparent 70%);-webkit-mask:radial-gradient(ellipse at center, black 30%, transparent 70%);pointer-events:none}
.page-header-inner{position:relative;z-index:2;max-width:800px;margin:0 auto}
.page-tag{display:inline-flex;align-items:center;gap:8px;background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.3);color:var(--orange);font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;padding:8px 16px;border-radius:999px;letter-spacing:1px;margin-bottom:20px;text-transform:uppercase}
.page-tag::before{content:'';width:6px;height:6px;border-radius:50%;background:var(--orange);box-shadow:0 0 12px var(--orange)}
.page-title{font-size:clamp(32px,5vw,56px);font-weight:900;letter-spacing:-1.5px;line-height:1.12;margin-bottom:18px}
.page-title .grad{background:linear-gradient(135deg, var(--orange), var(--pink), var(--purple));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;display:inline-block;padding-bottom:0.08em}
.page-sub{font-size:clamp(15px,1.6vw,18px);color:var(--text-2);max-width:560px;margin:0 auto;line-height:1.55}
.main-content{max-width:1100px;margin:0 auto;padding:60px 32px 100px;min-height:40vh}
.sub-services{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,260px));gap:18px;justify-content:center}
.sub-card{background:var(--card);border:1px solid var(--border);border-radius:18px;overflow:hidden;transition:all 0.3s ease;display:flex;flex-direction:column}
.sub-card:hover{transform:translateY(-4px);border-color:var(--orange);box-shadow:0 12px 36px rgba(249,115,22,0.15)}
.sub-card-img{position:relative;aspect-ratio:1/1;overflow:hidden;background:var(--bg-2)}
.sub-card-img img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:opacity 0.45s ease, transform 0.6s ease}
.sub-card-img .img-base{opacity:1;z-index:1}
.sub-card-img .img-hover{opacity:0;z-index:2}
.sub-card:hover .img-base{opacity:0}
.sub-card:hover .img-hover{opacity:1;transform:scale(1.04)}
.sub-card-price{position:absolute;top:10px;right:10px;background:linear-gradient(135deg, var(--orange), var(--pink));color:#fff;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:800;padding:6px 12px;border-radius:999px;letter-spacing:0.3px;z-index:3;box-shadow:0 4px 16px rgba(249,115,22,0.35)}
.sub-card-body{padding:16px;display:flex;flex-direction:column;gap:12px}
.sub-card-title{font-size:15px;font-weight:800;letter-spacing:-0.3px;line-height:1.25;text-align:center}
.sub-card-cta{display:inline-flex;align-items:center;justify-content:center;gap:6px;background:linear-gradient(135deg, var(--orange), var(--pink));color:#fff;font-size:13px;font-weight:700;padding:11px 18px;border-radius:999px;transition:all 0.25s}
.sub-card-cta:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(249,115,22,0.3)}
.sub-card-cta::after{content:'→';font-size:14px}
.footer{border-top:1px solid var(--border);padding:32px;text-align:center;color:var(--text-3);font-size:13px}
.footer a{color:var(--orange)}
@media(max-width:640px){.topnav{padding:12px 18px}.page-header{padding:60px 20px 40px}.main-content{padding:40px 20px 60px}}
</style>
</head>
<body>

<nav class="topnav">
  <a href="personalizar-arte-mural.html" class="topnav-logo">
    <img src="logo-kodara.jpeg" alt="Kodara SE">
    <div>Kodara <span>PRINT</span></div>
  </a>
  <a href="personalizar-arte-mural.html" class="topnav-back">← Volver a Arte Mural</a>
</nav>

<header class="page-header">
  <div class="page-header-inner">
    <div class="page-tag">Arte Mural · Marco de Madera</div>
    <h1 class="page-title">
      Personaliza tu <span class="grad">marco de madera</span>.
    </h1>
    <p class="page-sub">
      Pósteres en marco de madera natural con cristal. Listos para colgar — sin clavos, sin complicaciones.
    </p>
  </div>
</header>

<main class="main-content">
  <div class="sub-services">

'''

for key, full, short, lower, base, hover, costo, precio_desde in products:
    catalogo += f'''    <article class="sub-card">
      <div class="sub-card-img">
        <span class="sub-card-price">Desde ${precio_desde}</span>
        <img class="img-base" src="{base}" alt="{full}">
        <img class="img-hover" src="{hover}" alt="{full} en pared">
      </div>
      <div class="sub-card-body">
        <h2 class="sub-card-title">{full}</h2>
        <a href="pedido-marco-madera-{key}.html" class="sub-card-cta">Personalizar</a>
      </div>
    </article>

'''

catalogo += '''  </div>
</main>

<footer class="footer">
  © 2026 Kodara SE · <a href="index.html">kodarase.com</a>
</footer>

</body>
</html>
'''

with open(os.path.join(OUT_DIR, "arte-mural-marco-madera.html"), "w", encoding="utf-8") as f:
    f.write(catalogo)
print("OK CATÁLOGO  arte-mural-marco-madera.html  (5 tarjetas con doble imagen + Desde $X)")

# ========== 2. PÁGINAS DE PEDIDO (basadas en pedido-impresion-artistica.html) ==========
template_path = os.path.join(OUT_DIR, "pedido-impresion-artistica.html")
with open(template_path, "r", encoding="utf-8") as f:
    template = f.read()

for key, full, short, lower, base, hover, costo, precio_desde in products:
    pedido_file = f"pedido-marco-madera-{key}.html"
    new_html = template
    new_html = new_html.replace(
        "<title>Hacer mi pedido · Impresión Artística · Kodara Print</title>",
        f"<title>Hacer mi pedido · {full} · Kodara Print</title>"
    )
    new_html = new_html.replace(
        'href="arte-mural-impresion-artistica.html"',
        'href="arte-mural-marco-madera.html"'
    )
    # Texto del botón Volver
    new_html = new_html.replace(
        '<a href="arte-mural-marco-madera.html" class="topnav-back">← Volver</a>',
        '<a href="arte-mural-marco-madera.html" class="topnav-back">← Volver a Marco de Madera</a>'
    )
    new_html = new_html.replace(
        '<div class="page-tag">Pedido · Impresión Artística</div>',
        f'<div class="page-tag">Pedido · {full}</div>'
    )
    new_html = new_html.replace(
        'value="Nuevo pedido · Impresión Artística · Kodara Print"',
        f'value="Nuevo pedido · {full} · Kodara Print"'
    )

    with open(os.path.join(OUT_DIR, pedido_file), "w", encoding="utf-8") as f:
        f.write(new_html)
    print(f"OK PEDIDO    {pedido_file}  (con precios placeholder de Impresión Artística — actualizar cuando Angel dé costos)")

print("\nDONE")
print("\n⚠️  Los precios en las páginas de pedido son TEMPORALES (heredados de Impresión Artística $17-$51).")
print("   Cuando Angel mande los costos min-max de cada producto, ejecutar el script de precios.")
