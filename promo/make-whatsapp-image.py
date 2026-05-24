"""
Genera la imagen WhatsApp con texto overlay perfecto en español.
Sin precios, enfocada en público latino (negocio o casa).
"""
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = r"C:\Users\lucie\kodara-se\promo"
os.makedirs(OUT_DIR, exist_ok=True)

# Imagen limpia (sin texto) de la latina con poster
src_url = "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_192413_461a8bef-8a2d-4252-8836-a6d87d5264dd.png"
src_path = os.path.join(OUT_DIR, "_whatsapp-clean.png")
out_path = os.path.join(OUT_DIR, "whatsapp-latinos.png")

# Descargar
urllib.request.urlretrieve(src_url, src_path)
img = Image.open(src_path).convert("RGB")
W, H = img.size
print(f"Imagen base: {W}x{H}")

# Upscale a 1080x1080 para WhatsApp HD
img = img.resize((1080, 1080), Image.LANCZOS)
W, H = 1080, 1080

# Capa de oscurecimiento abajo para legibilidad del texto
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
# Gradiente abajo (~40% inferior)
for i in range(int(H * 0.55), H):
    alpha = int(((i - H * 0.55) / (H * 0.45)) * 180)
    od.rectangle([(0, i), (W, i + 1)], fill=(0, 0, 0, alpha))

img_rgba = img.convert("RGBA")
img_rgba = Image.alpha_composite(img_rgba, overlay)
draw = ImageDraw.Draw(img_rgba)

# Buscar fuentes del sistema Windows
def find_font(names, size):
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except:
            continue
    return ImageFont.load_default()

font_serif_bold = find_font(["georgiab.ttf", "Georgia Bold.ttf", "GeorgiaBold.ttf", "georgia.ttf"], 78)
font_serif_med = find_font(["georgia.ttf", "Georgia.ttf"], 42)
font_sans = find_font(["arialbd.ttf", "Arial Bold.ttf", "arial.ttf"], 28)

# TEXTO 1 (top sobre escena, pero en zona inferior con overlay)
text1 = "PARA TU CASA"
text2 = "O TU NEGOCIO"
text3 = "Diseñamos e imprimimos lo que imagines"
text4 = "kodarase.com"

# Posiciones (zona inferior con overlay)
y_text1 = int(H * 0.62)
y_text2 = int(H * 0.71)
y_text3 = int(H * 0.83)
y_text4 = int(H * 0.92)

def draw_centered(draw, text, y, font, fill, shadow=True):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    x = (W - w) // 2 - bbox[0]
    if shadow:
        draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 180))
    draw.text((x, y), text, font=font, fill=fill)

# Texto principal (cream)
draw_centered(draw, text1, y_text1, font_serif_bold, (255, 248, 230, 255))
draw_centered(draw, text2, y_text2, font_serif_bold, (255, 248, 230, 255))

# Texto subtítulo (gold)
draw_centered(draw, text3, y_text3, font_serif_med, (212, 169, 119, 255))

# URL (blanco)
draw_centered(draw, text4, y_text4, font_sans, (255, 255, 255, 230))

# Guardar
img_final = img_rgba.convert("RGB")
img_final.save(out_path, "PNG", optimize=True, quality=95)
print(f"OK guardado: {out_path}")
print(f"Tamaño: {img_final.size}")
print(f"Peso: {os.path.getsize(out_path)/1024:.1f} KB")

# Limpiar archivo temporal
os.remove(src_path)
print("Listo!")
