"""
Construye la categoria Madera:
- arte-mural-madera.html (sub-catalogo con 1 card)
- pedido-madera.html (con grosor 10mm/20mm que cambia precio - igual que Lienzos)
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"C:\Users\lucie\kodara-se"

IMG_BASE = "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260524_073703_029a598a-e3c5-4549-ae04-c3432678aacd.png"
IMG_HOVER = "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260524_073711_a540df9a-668d-470e-9502-7fe0fc421bc1.png"

# 14 tamanos (igual que Lienzos)
SIZES = [
    ("20x20 cm / 8x8\"",     "20 × 20 cm  ·  8 × 8\"  (cuadrado)",  "pequenos"),
    ("25x25 cm / 10x10\"",   "25 × 25 cm  ·  10 × 10\"  (cuadrado)", "pequenos"),
    ("30x30 cm / 12x12\"",   "30 × 30 cm  ·  12 × 12\"  (cuadrado)", "pequenos"),
    ("30x40 cm / 12x16\"",   "30 × 40 cm  ·  12 × 16\"",             "pequenos"),
    ("40x40 cm / 16x16\"",   "40 × 40 cm  ·  16 × 16\"  (cuadrado)", "medianos"),
    ("40x50 cm / 16x20\"",   "40 × 50 cm  ·  16 × 20\"",             "medianos"),
    ("40x60 cm / 16x24\"",   "40 × 60 cm  ·  16 × 24\"",             "medianos"),
    ("50x50 cm / 20x20\"",   "50 × 50 cm  ·  20 × 20\"  (cuadrado)", "medianos"),
    ("50x70 cm / 20x28\"",   "50 × 70 cm  ·  20 × 28\"",             "medianos"),
    ("60x60 cm / 24x24\"",   "60 × 60 cm  ·  24 × 24\"  (cuadrado)", "grandes"),
    ("60x80 cm / 24x32\"",   "60 × 80 cm  ·  24 × 32\"",             "grandes"),
    ("60x90 cm / 24x36\"",   "60 × 90 cm  ·  24 × 36\"",             "grandes"),
    ("70x70 cm / 28x28\"",   "70 × 70 cm  ·  28 × 28\"  (cuadrado)", "grandes"),
    ("70x100 cm / 28x40\"",  "70 × 100 cm  ·  28 × 40\"",            "grandes"),
]

def interp(a, b, pos, total):
    return a + (b - a) * pos / (total - 1)

def price(cost_min, cost_max, ship_min, ship_max, pos, total=14):
    cost = interp(cost_min, cost_max, pos, total)
    ship = interp(ship_min, ship_max, pos, total)
    return round((cost + ship) * 2)

# 10mm: cost $18.73 - $97.43, envio $21 - $32
prices_10 = [price(18.73, 97.43, 21.00, 32.00, i) for i in range(14)]
# 20mm: cost $28.09 - $146.15, envio $21 - $32
prices_20 = [price(28.09, 146.15, 21.00, 32.00, i) for i in range(14)]

print("10mm:", prices_10)
print("20mm:", prices_20)


# ===== SUB-CATALOGO arte-mural-madera.html =====
SUB_CATALOG = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Impresiones en madera · Kodara Print Studio</title>
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
.sub-card-price{{position:absolute;top:10px;right:10px;background:linear-gradient(135deg, var(--orange), var(--pink));color:#fff;font-family:'JetBrains Mono',monospace;font-size:12px;font-weight:800;padding:6px 12px;border-radius:999px;letter-spacing:0.3px;z-index:3;box-shadow:0 4px 16px rgba(249,115,22,0.35)}}
.sub-card-body{{padding:16px;display:flex;flex-direction:column;gap:12px}}
.sub-card-title{{font-size:15px;font-weight:800;letter-spacing:-0.3px;line-height:1.25;text-align:center}}
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
  <a href="personalizar-arte-mural.html" class="topnav-logo">
    <img src="logo-kodara.jpeg" alt="Kodara SE">
    <div>Kodara <span>PRINT</span></div>
  </a>
  <a href="personalizar-arte-mural.html" class="topnav-back">← Volver a Arte Mural</a>
</nav>

<header class="page-header">
  <div class="page-header-inner">
    <div class="page-tag">Arte Mural · Impresiones en madera</div>
    <h1 class="page-title">
      Personaliza tu <span class="grad">impresión en madera</span>.
    </h1>
    <p class="page-sub">
      Panel de madera natural con tu diseño impreso. Acabado cálido, sólido y elegante. Listo para colgar.
    </p>
  </div>
</header>

<main class="main-content">
  <div class="sub-services">

    <article class="sub-card">
      <div class="sub-card-img">
        <span class="sub-card-price">Desde ${prices_10[0]}</span>
        <img class="img-base" src="{IMG_BASE}" alt="Impresiones en madera">
        <img class="img-hover" src="{IMG_HOVER}" alt="Impresiones en madera en pared">
      </div>
      <div class="sub-card-body">
        <h2 class="sub-card-title">Impresiones en madera</h2>
        <a href="pedido-madera.html" class="sub-card-cta">Personalizar</a>
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

with open(os.path.join(OUT_DIR, "arte-mural-madera.html"), "w", encoding="utf-8") as f:
    f.write(SUB_CATALOG)
print("OK arte-mural-madera.html")


# ===== PEDIDO con GROSOR variable (igual que Lienzos) =====
groups = {"pequenos": [], "medianos": [], "grandes": []}
for i, (val, label, group) in enumerate(SIZES):
    p10 = prices_10[i]
    p20 = prices_20[i]
    groups[group].append(
        f'        <option data-price-10="{p10}" data-price-20="{p20}" value="{val}">{label}</option>'
    )

options_html = f'''      <optgroup label="Tamaños pequeños">
{chr(10).join(groups["pequenos"])}
      </optgroup>
      <optgroup label="Tamaños medianos">
{chr(10).join(groups["medianos"])}
      </optgroup>
      <optgroup label="Tamaños grandes">
{chr(10).join(groups["grandes"])}
      </optgroup>'''

PEDIDO = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hacer mi pedido · Impresiones en madera · Kodara Print</title>
<link rel="icon" type="image/jpeg" href="logo-kodara.jpeg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#060B18;--bg-2:#0A1424;--card:#0F1A2E;--card-2:#131F36;--border:rgba(255,255,255,0.06);--border-2:rgba(255,255,255,0.1);--text:#fff;--text-2:#B8C0D0;--text-3:#6B7689;--orange:#F97316;--orange-light:#FB923C;--pink:#EC4899;--purple:#7C3AED;--yellow:#F59E0B;--green:#10B981}}
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
.page-header{{position:relative;padding:60px 32px 40px;text-align:center;background:radial-gradient(ellipse at top, rgba(124,58,237,0.12), transparent 60%),radial-gradient(ellipse at bottom, rgba(249,115,22,0.08), transparent 60%),var(--bg);border-bottom:1px solid var(--border)}}
.page-header-inner{{position:relative;z-index:2;max-width:800px;margin:0 auto}}
.page-tag{{display:inline-flex;align-items:center;gap:8px;background:rgba(249,115,22,0.1);border:1px solid rgba(249,115,22,0.3);color:var(--orange);font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;padding:8px 16px;border-radius:999px;letter-spacing:1px;margin-bottom:20px;text-transform:uppercase}}
.page-tag::before{{content:'';width:6px;height:6px;border-radius:50%;background:var(--orange);box-shadow:0 0 12px var(--orange)}}
.page-title{{font-size:clamp(28px,4vw,44px);font-weight:900;letter-spacing:-1.2px;line-height:1.15;margin-bottom:14px}}
.page-title .grad{{background:linear-gradient(135deg, var(--orange), var(--pink), var(--purple));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;display:inline-block;padding-bottom:0.08em}}
.page-sub{{font-size:15px;color:var(--text-2);max-width:540px;margin:0 auto;line-height:1.55}}
.hero-shipping{{display:inline-flex;align-items:center;gap:10px;margin-top:22px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.35);border-radius:999px;padding:10px 22px;font-size:14px;color:#10B981;font-weight:700;box-shadow:0 4px 16px rgba(16,185,129,0.15)}}
.hero-shipping strong{{color:#10B981;font-weight:800}}
.shipping-icon{{font-size:18px}}
.form-wrap{{max-width:760px;margin:0 auto;padding:50px 24px 80px}}
.form-step{{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:28px;margin-bottom:20px}}
.step-num{{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;border-radius:50%;background:linear-gradient(135deg, var(--orange), var(--pink));color:#fff;font-weight:800;font-size:14px;font-family:'JetBrains Mono',monospace}}
.step-head{{display:flex;align-items:center;gap:14px;margin-bottom:6px}}
.step-title{{font-size:20px;font-weight:800;letter-spacing:-0.3px}}
.step-sub{{color:var(--text-3);font-size:13px;margin-bottom:22px;padding-left:44px}}
.size-select{{width:100%;background:var(--bg-2);border:2px solid var(--border-2);border-radius:14px;padding:16px 18px;color:var(--text);font-family:inherit;font-size:15px;font-weight:600;cursor:pointer;transition:border 0.2s;appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='8' viewBox='0 0 14 8'%3E%3Cpath fill='%23F97316' d='M7 8L0 0h14z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 18px center;padding-right:50px}}
.size-select:focus{{outline:none;border-color:var(--orange)}}
.size-select optgroup{{font-weight:800;color:var(--orange-light);background:var(--bg)}}
.size-select option{{color:var(--text);background:var(--bg-2);padding:8px;font-weight:500}}
.price-box{{display:flex;align-items:center;justify-content:space-between;gap:14px;background:linear-gradient(135deg, rgba(249,115,22,0.08), rgba(236,72,153,0.08));border:1px solid rgba(249,115,22,0.25);border-radius:14px;padding:18px 22px;margin-top:14px;transition:all 0.3s ease}}
.price-box.active{{border-color:var(--orange);background:linear-gradient(135deg, rgba(249,115,22,0.15), rgba(236,72,153,0.12))}}
.price-label{{font-size:12px;color:var(--text-3);font-weight:700;letter-spacing:1px;text-transform:uppercase}}
.price-amount{{font-size:clamp(28px,4vw,36px);font-weight:900;font-family:'JetBrains Mono',monospace;background:linear-gradient(135deg, var(--orange), var(--pink));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;line-height:1}}
.price-amount.empty{{background:none;-webkit-text-fill-color:var(--text-3);color:var(--text-3);font-size:16px;font-weight:600}}
.orient-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.orient-opt{{cursor:pointer;background:var(--bg-2);border:2px solid var(--border-2);border-radius:14px;padding:20px;text-align:center;transition:all 0.2s;display:flex;flex-direction:column;align-items:center;gap:12px}}
.orient-opt:hover{{border-color:var(--orange-light)}}
.orient-opt input{{display:none}}
.orient-opt:has(input:checked){{border-color:var(--orange);background:rgba(249,115,22,0.08)}}
.orient-icon{{width:48px;height:64px;background:linear-gradient(135deg,var(--card-2),var(--bg));border:1px solid var(--border-2);border-radius:6px}}
.orient-icon.horizontal{{width:64px;height:48px}}
.orient-label{{font-weight:700;font-size:14px}}
.grosor-grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
.grosor-opt{{cursor:pointer;background:var(--bg-2);border:2px solid var(--border-2);border-radius:14px;padding:20px;text-align:center;transition:all 0.2s;display:flex;flex-direction:column;align-items:center;gap:8px}}
.grosor-opt:hover{{border-color:var(--orange-light)}}
.grosor-opt input{{display:none}}
.grosor-opt:has(input:checked){{border-color:var(--orange);background:rgba(249,115,22,0.08)}}
.grosor-3d{{display:flex;align-items:flex-end;height:48px}}
.grosor-side{{background:linear-gradient(180deg, #D4A977, #8B6F3A);border-radius:2px 2px 0 0;height:36px}}
.grosor-side.s10{{width:10px}}
.grosor-side.s20{{width:22px}}
.grosor-front{{background:#D4A977;border:1px solid #8B6F3A;height:48px;border-left:none;width:90px}}
.grosor-label{{font-weight:700;font-size:14px;margin-top:8px}}
.grosor-desc{{font-size:11px;color:var(--text-3);font-family:'JetBrains Mono',monospace;letter-spacing:0.5px}}
.upload-zone{{display:flex;flex-direction:column;align-items:center;justify-content:center;border:2px dashed var(--border-2);border-radius:14px;padding:40px 20px;text-align:center;cursor:pointer;transition:all 0.2s;background:var(--bg-2);width:100%;min-height:200px}}
.upload-zone:hover{{border-color:var(--orange);background:rgba(249,115,22,0.04)}}
.upload-zone.dragover{{border-color:var(--orange);background:rgba(249,115,22,0.08);transform:scale(1.01)}}
.upload-zone.uploading{{border-color:var(--orange);background:rgba(249,115,22,0.04);cursor:wait}}
.upload-zone.done{{border-color:var(--green);background:rgba(16,185,129,0.05)}}
.upload-icon{{font-size:42px;margin-bottom:10px;opacity:0.75}}
.upload-text{{font-weight:700;font-size:15px;margin-bottom:6px}}
.upload-hint{{font-size:12px;color:var(--text-3)}}
.upload-zone input[type=file]{{display:none}}
.upload-progress{{display:none;width:100%;max-width:300px;margin-top:14px;height:8px;background:var(--bg);border-radius:999px;overflow:hidden}}
.upload-progress-bar{{height:100%;background:linear-gradient(90deg, var(--orange), var(--pink));width:0%;transition:width 0.3s ease}}
.upload-status{{margin-top:12px;font-size:13px;font-family:'JetBrains Mono',monospace;font-weight:700;color:var(--orange)}}
.upload-zone.done .upload-status{{color:var(--green)}}
.upload-preview{{display:none;max-width:120px;max-height:120px;border-radius:10px;margin-top:14px;border:2px solid var(--green)}}
.upload-clear{{display:none;margin-top:12px;background:transparent;border:1px solid var(--border-2);color:var(--text-3);font-size:12px;padding:6px 14px;border-radius:999px;cursor:pointer}}
.upload-clear:hover{{color:var(--text);border-color:var(--text-3)}}
.field{{margin-bottom:14px}}
.field label{{display:block;font-size:12px;font-weight:700;color:var(--text-2);margin-bottom:6px;letter-spacing:0.3px;text-transform:uppercase}}
.field input,.field textarea{{width:100%;background:var(--bg-2);border:1px solid var(--border-2);border-radius:12px;padding:14px 16px;color:var(--text);font-family:inherit;font-size:14px;transition:border 0.2s}}
.field input:focus,.field textarea:focus{{outline:none;border-color:var(--orange)}}
.field textarea{{resize:vertical;min-height:90px}}
.field-row{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
.field input:not(:placeholder-shown):invalid,.field textarea:not(:placeholder-shown):invalid{{border-color:#EF4444}}
.field input:not(:placeholder-shown):valid{{border-color:rgba(16,185,129,0.4)}}
.form-alert{{display:none;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.4);color:#FCA5A5;border-radius:12px;padding:14px 18px;font-size:14px;font-weight:600;margin-bottom:16px;text-align:center}}
.form-alert.show{{display:block}}
.submit-btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:linear-gradient(135deg, var(--orange), var(--pink));color:#fff;font-size:15px;font-weight:800;padding:18px 36px;border-radius:999px;border:none;cursor:pointer;width:100%;transition:all 0.25s;font-family:inherit}}
.submit-btn:hover{{transform:translateY(-2px);box-shadow:0 14px 40px rgba(249,115,22,0.35)}}
.submit-btn::after{{content:'→';font-size:17px}}
.privacy-note{{text-align:center;font-size:11px;color:var(--text-3);margin-top:16px}}
.privacy-note a{{color:var(--orange)}}
.footer{{border-top:1px solid var(--border);padding:32px;text-align:center;color:var(--text-3);font-size:13px}}
.footer a{{color:var(--orange)}}
@media(max-width:640px){{.topnav{{padding:12px 18px}}.form-wrap{{padding:32px 16px 60px}}.form-step{{padding:20px}}.field-row{{grid-template-columns:1fr}}}}
.form-step.locked{{opacity:0.42;pointer-events:none;filter:grayscale(0.4);position:relative;transition:all 0.3s ease}}
.form-step.locked::after{{content:'\\1F512  Completa el paso anterior';position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.92);color:#fff;padding:12px 24px;border-radius:999px;font-size:13px;font-weight:700;pointer-events:none;white-space:nowrap;backdrop-filter:blur(8px);border:1px solid rgba(255,255,255,0.15);box-shadow:0 8px 24px rgba(0,0,0,0.4);z-index:10}}
.form-step.unlocked-anim{{animation:stepUnlock 0.5s ease}}
@keyframes stepUnlock{{from{{transform:translateY(-6px);opacity:0.6}}to{{transform:translateY(0);opacity:1}}}}
</style>
</head>
<body>

<nav class="topnav">
  <a href="arte-mural-madera.html" class="topnav-logo">
    <img src="logo-kodara.jpeg" alt="Kodara SE">
    <div>Kodara <span>PRINT</span></div>
  </a>
  <a href="arte-mural-madera.html" class="topnav-back">← Volver a Impresiones en madera</a>
</nav>

<header class="page-header">
  <div class="page-header-inner">
    <div class="page-tag">Pedido · Impresiones en madera</div>
    <h1 class="page-title">Haz tu <span class="grad">impresión en madera</span>.</h1>
    <p class="page-sub">Elige orientación, grosor, tamaño, sube tu imagen y déjanos tus datos. Nosotros nos encargamos del resto.</p>
    <div class="hero-shipping"><span class="shipping-icon">🚚</span><strong>Envío gratis</strong></div>
  </div>
</header>

<form class="form-wrap" action="https://api.web3forms.com/submit" method="POST">
  <input type="hidden" name="access_key" value="2e5a1c54-e4bf-41f4-b04c-7f4c30dace33">
  <input type="hidden" name="subject" value="Nuevo pedido · Impresiones en madera · Kodara Print">
  <input type="hidden" name="from_name" value="Kodara Print Studio">

  <!-- 1 · ORIENTACIÓN -->
  <div class="form-step">
    <div class="step-head"><div class="step-num">1</div><div class="step-title">Orientación</div></div>
    <p class="step-sub">Vertical u horizontal según tu imagen.</p>
    <div class="orient-grid">
      <label class="orient-opt">
        <input type="radio" name="orientacion" value="Vertical" required>
        <div class="orient-icon"></div>
        <div class="orient-label">Vertical</div>
      </label>
      <label class="orient-opt">
        <input type="radio" name="orientacion" value="Horizontal">
        <div class="orient-icon horizontal"></div>
        <div class="orient-label">Horizontal</div>
      </label>
    </div>
  </div>

  <!-- 2 · GROSOR -->
  <div class="form-step">
    <div class="step-head"><div class="step-num">2</div><div class="step-title">Grosor del panel</div></div>
    <p class="step-sub">El grosor cambia el precio. 10mm = más fino y económico. 20mm = más sólido y luxury.</p>
    <div class="grosor-grid">
      <label class="grosor-opt">
        <input type="radio" name="grosor" value="10mm" required>
        <div class="grosor-3d"><div class="grosor-side s10"></div><div class="grosor-front" style="width:80px"></div></div>
        <div class="grosor-label">10 mm</div>
        <div class="grosor-desc">Fino · más económico</div>
      </label>
      <label class="grosor-opt">
        <input type="radio" name="grosor" value="20mm">
        <div class="grosor-3d"><div class="grosor-side s20"></div><div class="grosor-front" style="width:80px"></div></div>
        <div class="grosor-label">20 mm</div>
        <div class="grosor-desc">Grueso · luxury</div>
      </label>
    </div>
  </div>

  <!-- 3 · TAMAÑO -->
  <div class="form-step">
    <div class="step-head"><div class="step-num">3</div><div class="step-title">Tamaño del panel</div></div>
    <p class="step-sub">14 tamaños disponibles. El precio cambia según el grosor que elegiste arriba.</p>
    <select class="size-select" name="tamano" id="size-select" required>
      <option value="" disabled selected>— Selecciona un tamaño —</option>
{options_html}
    </select>
    <div class="price-box" id="price-box">
      <div class="price-label">Precio</div>
      <div class="price-amount empty" id="price-amount">Elige grosor y tamaño</div>
    </div>
    <input type="hidden" name="precio" id="precio-hidden" value="">
  </div>

  <!-- 4 · IMAGEN -->
  <div class="form-step">
    <div class="step-head"><div class="step-num">4</div><div class="step-title">Tu imagen</div></div>
    <p class="step-sub">Sube la foto, diseño o ilustración que quieres imprimir. A más resolución, mejor impresión.</p>
    <label class="upload-zone" id="upload-zone">
      <input type="file" id="file-input" accept="image/jpeg,image/png,image/webp">
      <div class="upload-icon" id="upload-icon">📁</div>
      <div class="upload-text" id="upload-text">Arrastra tu imagen aquí o haz clic para elegirla</div>
      <div class="upload-hint" id="upload-hint">JPG, PNG, WEBP · hasta 10 MB · Si pesa más, la comprimimos automáticamente</div>
      <div class="upload-progress" id="upload-progress"><div class="upload-progress-bar" id="upload-progress-bar"></div></div>
      <div class="upload-status" id="upload-status"></div>
      <img class="upload-preview" id="upload-preview" alt="">
      <button type="button" class="upload-clear" id="upload-clear">Cambiar imagen</button>
    </label>
    <input type="hidden" name="imagen_url" id="imagen-url" required>
  </div>

  <!-- 5 · DATOS DE ENVÍO -->
  <div class="form-step">
    <div class="step-head"><div class="step-num">5</div><div class="step-title">Tus datos de envío</div></div>
    <p class="step-sub">Necesitamos estos datos para enviarte tu pedido.</p>
    <div class="field-row">
      <div class="field"><label for="nombre">Nombre</label><input type="text" id="nombre" name="nombre" required minlength="2" maxlength="40" pattern="[A-Za-zÀ-ÿñÑ\\s'\\-]{{2,40}}" title="Solo letras."></div>
      <div class="field"><label for="apellido">Apellido</label><input type="text" id="apellido" name="apellido" required minlength="2" maxlength="60" pattern="[A-Za-zÀ-ÿñÑ\\s'\\-]{{2,60}}" title="Solo letras."></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="direccion-1">Dirección, línea 1</label><input type="text" id="direccion-1" name="direccion_1" required minlength="5" maxlength="100" placeholder="Calle, número"></div>
      <div class="field"><label for="email">Correo electrónico</label><input type="email" id="email" name="email" required maxlength="80" pattern="[A-Za-z0-9._%+\\-]+@[A-Za-z0-9.\\-]+\\.[A-Za-z]{{2,}}" placeholder="tucorreo@ejemplo.com"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="direccion-2">Dirección, línea 2 <span style="color:var(--text-3);font-weight:500;text-transform:none">(opcional)</span></label><input type="text" id="direccion-2" name="direccion_2" maxlength="100" placeholder="Piso, puerta, escalera"></div>
      <div class="field"><label for="empresa">Nombre de empresa <span style="color:var(--text-3);font-weight:500;text-transform:none">(opcional)</span></label><input type="text" id="empresa" name="empresa" maxlength="60"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="codigo-postal">Código postal</label><input type="text" id="codigo-postal" name="codigo_postal" required minlength="3" maxlength="10" pattern="[A-Za-z0-9\\s\\-]{{3,10}}" placeholder="08001"></div>
      <div class="field"><label for="telefono">Teléfono</label><input type="tel" id="telefono" name="telefono" required minlength="7" maxlength="20" pattern="[\\d\\s\\(\\)\\-\\+]{{7,20}}" placeholder="+1 (201) 555-0123"></div>
    </div>
    <div class="field-row">
      <div class="field"><label for="ciudad">Ciudad</label><input type="text" id="ciudad" name="ciudad" required minlength="2" maxlength="60" pattern="[A-Za-zÀ-ÿñÑ\\s'\\-\\.]{{2,60}}"></div>
      <div class="field"><label for="estado">Estado / Provincia / Región</label><input type="text" id="estado" name="estado" required minlength="2" maxlength="60" pattern="[A-Za-zÀ-ÿñÑ\\s'\\-\\.]{{2,60}}"></div>
    </div>
    <div class="field"><label for="pais">País</label><input type="text" id="pais" name="pais" required minlength="2" maxlength="60" pattern="[A-Za-zÀ-ÿñÑ\\s'\\-\\.]{{2,60}}" placeholder="España / Estados Unidos / México..."></div>
    <div class="field"><label for="notas">Notas / instrucciones <span style="color:var(--text-3);font-weight:500;text-transform:none">(opcional)</span></label><textarea id="notas" name="notas" placeholder="¿Algo que tengamos que tener en cuenta?"></textarea></div>
  </div>

  <div class="form-alert" id="form-alert"></div>
  <button type="submit" class="submit-btn" id="submit-btn">Enviar pedido</button>
  <p class="privacy-note">Al enviar aceptas nuestra <a href="politica-privacidad.html">política de privacidad</a>.</p>
</form>

<footer class="footer">© 2026 Kodara SE · <a href="index.html">kodarase.com</a></footer>

<script>
const CLOUD_NAME = 'dxzppmgqb';
const UPLOAD_PRESET = 'kodara_pedidos';
const zone = document.getElementById('upload-zone');
const input = document.getElementById('file-input');
const icon = document.getElementById('upload-icon');
const text = document.getElementById('upload-text');
const hint = document.getElementById('upload-hint');
const progress = document.getElementById('upload-progress');
const progressBar = document.getElementById('upload-progress-bar');
const status = document.getElementById('upload-status');
const preview = document.getElementById('upload-preview');
const clearBtn = document.getElementById('upload-clear');
const urlField = document.getElementById('imagen-url');
['dragover','dragenter'].forEach(evt=>zone.addEventListener(evt,e=>{{e.preventDefault();if(!zone.classList.contains('uploading')&&!zone.classList.contains('done'))zone.classList.add('dragover');}}));
['dragleave','dragend','drop'].forEach(evt=>zone.addEventListener(evt,e=>{{e.preventDefault();zone.classList.remove('dragover');}}));
zone.addEventListener('drop',e=>{{if(e.dataTransfer.files.length>0)handleFile(e.dataTransfer.files[0]);}});
input.addEventListener('change',e=>{{if(e.target.files.length>0)handleFile(e.target.files[0]);}});
clearBtn.addEventListener('click',e=>{{e.preventDefault();e.stopPropagation();resetZone();}});
function resetZone(){{zone.classList.remove('uploading','done');icon.textContent='📁';icon.style.display='';text.textContent='Arrastra tu imagen aquí o haz clic para elegirla';text.style.display='';hint.style.display='';progress.style.display='none';progressBar.style.width='0%';status.textContent='';preview.style.display='none';preview.src='';clearBtn.style.display='none';urlField.value='';input.value='';}}
const MAX_BYTES = 10 * 1024 * 1024;
async function compressImage(file, maxBytes){{
  const img = await new Promise((res,rej)=>{{const i=new Image();i.onload=()=>res(i);i.onerror=rej;i.src=URL.createObjectURL(file);}});
  const canvas=document.createElement('canvas');canvas.width=img.naturalWidth;canvas.height=img.naturalHeight;
  canvas.getContext('2d').drawImage(img,0,0);URL.revokeObjectURL(img.src);
  for(const q of [0.92,0.85,0.78,0.7,0.6,0.5]){{
    const blob = await new Promise(r=>canvas.toBlob(r,'image/jpeg',q));
    if(blob && blob.size <= maxBytes) return new File([blob], file.name.replace(/\\.[^.]+$/,'')+'.jpg',{{type:'image/jpeg'}});
  }}
  return null;
}}
async function handleFile(originalFile){{
  if(!originalFile.type.match(/^image\\/(jpeg|png|webp)$/)){{status.textContent='✗ Solo JPG, PNG o WEBP';status.style.color='#EF4444';return;}}
  let file = originalFile;
  if(file.size > MAX_BYTES){{
    zone.classList.remove('done');zone.classList.add('uploading');
    icon.textContent='🗜️';text.textContent='Comprimiendo imagen...';hint.style.display='none';
    progress.style.display='none';status.style.color='';status.textContent='Reduciendo tamaño...';clearBtn.style.display='none';
    try{{
      const compressed = await compressImage(originalFile, MAX_BYTES);
      if(!compressed){{zone.classList.remove('uploading');status.textContent='✗ Imagen muy grande';status.style.color='#EF4444';icon.textContent='⚠️';text.textContent='Haz clic para reintentar';hint.style.display='block';return;}}
      file = compressed;
    }}catch(e){{zone.classList.remove('uploading');status.textContent='✗ Error: '+e.message;status.style.color='#EF4444';return;}}
  }}
  zone.classList.remove('done');zone.classList.add('uploading');
  icon.textContent='⏳';text.textContent='Subiendo tu imagen...';hint.style.display='none';
  progress.style.display='block';progressBar.style.width='0%';status.style.color='';status.textContent='0%';clearBtn.style.display='none';
  const formData = new FormData();
  formData.append('file', file);formData.append('upload_preset', UPLOAD_PRESET);
  const xhr = new XMLHttpRequest();
  xhr.open('POST', `https://api.cloudinary.com/v1_1/${{CLOUD_NAME}}/image/upload`);
  xhr.upload.onprogress=e=>{{if(e.lengthComputable){{const pct=Math.round((e.loaded/e.total)*100);progressBar.style.width=pct+'%';status.textContent=pct+'%';}}}};
  xhr.onload=()=>{{
    if(xhr.status===200){{
      const res = JSON.parse(xhr.responseText);
      urlField.value = res.secure_url;
      zone.classList.remove('uploading');zone.classList.add('done');
      icon.style.display='none';text.style.display='none';progress.style.display='none';
      preview.src = res.secure_url;preview.style.display='block';
      const sizeMB = (file.size/(1024*1024)).toFixed(1);
      status.textContent='✓ Imagen subida ('+sizeMB+' MB)';clearBtn.style.display='inline-block';
    }}else{{
      zone.classList.remove('uploading');
      let detail = 'HTTP '+xhr.status;
      try{{const errBody=JSON.parse(xhr.responseText);if(errBody&&errBody.error&&errBody.error.message)detail=errBody.error.message;}}catch(e){{}}
      status.textContent='✗ '+detail;status.style.color='#EF4444';progress.style.display='none';
      icon.textContent='⚠️';text.textContent='Haz clic para reintentar';hint.style.display='block';
    }}
  }};
  xhr.onerror=()=>{{zone.classList.remove('uploading');status.textContent='✗ Error de conexión';status.style.color='#EF4444';}};
  xhr.send(formData);
}}

// ===== PRECIO DINÁMICO (tamaño + grosor) =====
const sizeSelect = document.getElementById('size-select');
const priceBox = document.getElementById('price-box');
const priceAmount = document.getElementById('price-amount');
const precioHidden = document.getElementById('precio-hidden');
function updatePrice(){{
  const opt = sizeSelect.options[sizeSelect.selectedIndex];
  const grosor = document.querySelector('input[name="grosor"]:checked');
  if(!opt || !opt.value || !grosor){{
    priceAmount.textContent = 'Elige grosor y tamaño';
    priceAmount.classList.add('empty');
    priceBox.classList.remove('active');
    precioHidden.value = '';
    return;
  }}
  const price = grosor.value === '10mm' ? opt.dataset.price10 : opt.dataset.price20;
  priceAmount.textContent = '$' + price;
  priceAmount.classList.remove('empty');
  priceBox.classList.add('active');
  precioHidden.value = '$' + price + ' (' + grosor.value + ')';
}}
sizeSelect.addEventListener('change', updatePrice);
document.querySelectorAll('input[name="grosor"]').forEach(r => r.addEventListener('change', updatePrice));

const form = document.querySelector('form.form-wrap');
const alertBox = document.getElementById('form-alert');
function showAlert(msg){{
  alertBox.textContent = '⚠ ' + msg;
  alertBox.classList.add('show');
  alertBox.scrollIntoView({{behavior:'smooth',block:'center'}});
  setTimeout(()=>alertBox.classList.remove('show'), 6000);
}}
form.addEventListener('submit', (e) => {{
  const orient = form.querySelector('[name="orientacion"]:checked');
  if(!orient){{e.preventDefault();showAlert('Tienes que elegir orientación (paso 1).');return;}}
  const grosor = form.querySelector('[name="grosor"]:checked');
  if(!grosor){{e.preventDefault();showAlert('Tienes que elegir el grosor (paso 2).');return;}}
  const tamano = form.querySelector('[name="tamano"]');
  if(!tamano.value){{e.preventDefault();showAlert('Tienes que elegir un tamaño (paso 3).');tamano.focus();return;}}
  if(!urlField.value || !urlField.value.startsWith('https://res.cloudinary.com/')){{
    e.preventDefault();showAlert('Tienes que subir una imagen (paso 4).');zone.scrollIntoView({{behavior:'smooth',block:'center'}});return;
  }}
  if(zone.classList.contains('uploading')){{
    e.preventDefault();showAlert('Espera a que termine de subirse la imagen.');return;
  }}
}});
</script>

<script>
(function(){{
  const steps = Array.from(document.querySelectorAll('.form-step'));
  if (steps.length < 2) return;
  steps.forEach((s, i) => {{ if (i > 0) s.classList.add('locked'); }});
  function isStepComplete(step) {{
    const sel = step.querySelector('select[required]');
    if (sel && !sel.value) return false;
    const radios = step.querySelectorAll('input[type="radio"][required]');
    if (radios.length > 0) {{
      const name = radios[0].name;
      if (!step.querySelector(`input[name="${{name}}"]:checked`)) return false;
    }}
    const urlField = step.querySelector('#imagen-url');
    if (urlField) {{
      if (!urlField.value || !urlField.value.startsWith('https://res.cloudinary.com/')) return false;
    }}
    const inputs = step.querySelectorAll('input[required], textarea[required]');
    if (inputs.length > 0) {{
      for (const inp of inputs) {{
        if (!inp.value.trim()) return false;
        if (!inp.checkValidity()) return false;
      }}
    }}
    return true;
  }}
  function refreshLocks() {{
    let allValidUpToHere = true;
    steps.forEach((step, i) => {{
      if (i === 0) {{
        if (!isStepComplete(step)) allValidUpToHere = false;
        return;
      }}
      if (allValidUpToHere) {{
        if (step.classList.contains('locked')) {{
          step.classList.remove('locked');
          step.classList.add('unlocked-anim');
          setTimeout(() => step.classList.remove('unlocked-anim'), 500);
        }}
        if (!isStepComplete(step)) allValidUpToHere = false;
      }} else {{
        step.classList.add('locked');
      }}
    }});
  }}
  document.addEventListener('change', refreshLocks);
  document.addEventListener('input', refreshLocks);
  const urlField = document.getElementById('imagen-url');
  if (urlField) {{
    let lastVal = urlField.value;
    setInterval(() => {{
      if (urlField.value !== lastVal) {{
        lastVal = urlField.value;
        refreshLocks();
      }}
    }}, 500);
  }}
  refreshLocks();
}})();
</script>
</body>
</html>
'''

with open(os.path.join(OUT_DIR, "pedido-madera.html"), "w", encoding="utf-8") as f:
    f.write(PEDIDO)
print("OK pedido-madera.html")

print("\nDONE")
