# -*- coding: utf-8 -*-
"""Video promo v3 — desde cero con Unicode escape sequences que NO fallan."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, vfx
from moviepy.audio.fx import AudioFadeOut, AudioLoop
import os, random, shutil

W, H = 1080, 1920
FPS = 30

CREAM = (245, 239, 230)
CHARCOAL = (30, 25, 22)
GOLD = (201, 168, 76)
TERRACOTTA = (198, 107, 61)
WHITE = (255, 253, 248)
TEXT_DARK = (45, 38, 32)
TEXT_SOFT = (90, 80, 68)

# Use Unicode escape sequences for safety (no encoding issues)
N_ENE = "ñ"   # ñ
A_ACC = "á"   # á
E_ACC = "é"   # é
I_ACC = "í"   # í
O_ACC = "ó"   # ó
U_ACC = "ú"   # ú
MIDDLE_DOT = "·"  # ·

def font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

# Use Arial/Calibri for better Unicode coverage instead of Georgia
F_HUGE_SERIF = lambda s: font('C:/Windows/Fonts/georgiab.ttf', s)
F_ITAL_SERIF = lambda s: font('C:/Windows/Fonts/georgiai.ttf', s)
F_REG_SERIF  = lambda s: font('C:/Windows/Fonts/georgia.ttf', s)
F_BOLD       = lambda s: font('C:/Windows/Fonts/arialbd.ttf', s)
F_MONO       = lambda s: font('C:/Windows/Fonts/consolab.ttf', s)

def paper(w, h, base=CREAM):
    img = Image.new('RGB', (w, h), base)
    d = ImageDraw.Draw(img)
    random.seed(7)
    for _ in range(w * h // 600):
        x, y = random.randint(0, w-1), random.randint(0, h-1)
        shade = random.randint(-10, 5)
        c = (max(0, base[0]+shade), max(0, base[1]+shade), max(0, base[2]+shade))
        d.point((x, y), fill=c)
    return img

def center(d, text, y, fnt, color, w=W):
    bbox = d.textbbox((0,0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    d.text(((w - tw) // 2, y), text, font=fnt, fill=color)

os.makedirs('video-promo/frames-v3', exist_ok=True)

# ============== 01 APERTURA ==============
img = paper(W, H)
d = ImageDraw.Draw(img)
d.line([(W//2 - 80, 700), (W//2 + 80, 700)], fill=GOLD, width=2)
center(d, "PRESENTA", 740, F_REG_SERIF(28), TEXT_SOFT)
center(d, "KODARASE", int(H * 0.43), F_HUGE_SERIF(160), CHARCOAL)
center(d, "P R I N T   S T U D I O", int(H * 0.55), F_REG_SERIF(48), TERRACOTTA)
d.line([(W//2 - 80, int(H * 0.62)), (W//2 + 80, int(H * 0.62))], fill=GOLD, width=2)
center(d, "Tus recuerdos hechos arte", int(H * 0.65), F_ITAL_SERIF(36), TEXT_SOFT)
img.save('video-promo/frames-v3/01-apertura.png')
print("01-apertura OK")

# ============== PRODUCTOS ==============
def make_product_frame(prod_img_path, label, sublabel):
    """Frame del producto: imagen Higgsfield fullscreen + banner inferior con titulo."""
    prod = Image.open(prod_img_path).convert('RGB')
    src_w, src_h = prod.size
    src_ratio = src_w / src_h
    tgt_ratio = W / H
    if src_ratio > tgt_ratio:
        new_w = int(src_h * tgt_ratio)
        offset = (src_w - new_w) // 2
        prod = prod.crop((offset, 0, offset + new_w, src_h))
    else:
        new_h = int(src_w / tgt_ratio)
        offset = (src_h - new_h) // 2
        prod = prod.crop((0, offset, src_w, offset + new_h))
    prod = prod.resize((W, H), Image.LANCZOS)

    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(int(H * 0.78), H):
        progress = (y - int(H*0.78)) / (H - int(H*0.78))
        alpha = int(180 * progress ** 1.2)
        od.line([(0, y), (W, y)], fill=(20, 14, 10, alpha))

    img = Image.alpha_composite(prod.convert('RGBA'), overlay).convert('RGB')
    d = ImageDraw.Draw(img)
    d.line([(W//2 - 60, int(H * 0.83)), (W//2 + 60, int(H * 0.83))], fill=GOLD, width=2)
    # Use Bold Arial which has great Unicode coverage
    center(d, label, int(H * 0.86), F_BOLD(72), WHITE)
    if sublabel:
        center(d, sublabel, int(H * 0.93), F_BOLD(32), (220, 210, 195))
    return img

# Productos usando escape sequences seguros
TAMA_OS = "tama" + N_ENE + "os"
products = [
    ('01-lienzo-enmarcado.png', "Lienzos Enmarcados", "Madera natural " + MIDDLE_DOT + " 13 " + TAMA_OS),
    ('02-marco-madera.png',     "Marcos de Madera",   "Roble premium " + MIDDLE_DOT + " 22 " + TAMA_OS),
    ('03-aluminio.png',         "Impresi" + O_ACC + "n en Aluminio", "Met" + A_ACC + "lico moderno " + MIDDLE_DOT + " 18 " + TAMA_OS),
    ('04-plexiglas.png',        "Plexigl" + A_ACC + "s Brillante", "Cristal acr" + I_ACC + "lico " + MIDDLE_DOT + " 18 " + TAMA_OS),
    ('05-madera.png',           "Impresi" + O_ACC + "n en Madera", "Roble r" + U_ACC + "stico " + MIDDLE_DOT + " 18 " + TAMA_OS),
    ('06-espuma.png',           "Panel de Espuma", "Ligero " + MIDDLE_DOT + " 13 " + TAMA_OS),
]

for i, (pf, label, sub) in enumerate(products, start=2):
    img = make_product_frame(f'video-promo/productos-higgsfield/{pf}', label, sub)
    img.save(f'video-promo/frames-v3/0{i}-producto.png')
    print(f"0{i} {label} OK")

# ============== 08 OFERTA ==============
img = paper(W, H)
d = ImageDraw.Draw(img)
center(d, "PRIMERA COMPRA", int(H * 0.20), F_REG_SERIF(38), TERRACOTTA)
center(d, "20% OFF", int(H * 0.27), F_HUGE_SERIF(220), CHARCOAL)
d.line([(W//2 - 120, int(H * 0.50)), (W//2 + 120, int(H * 0.50))], fill=GOLD, width=2)
center(d, "tu primer pedido", int(H * 0.52), F_ITAL_SERIF(42), TEXT_SOFT)
box_w, box_h = 720, 180
box_x = (W - box_w) // 2
box_y = int(H * 0.62)
d.rounded_rectangle([box_x, box_y, box_x+box_w, box_y+box_h], radius=20, fill=TERRACOTTA)
d.rounded_rectangle([box_x+8, box_y+8, box_x+box_w-8, box_y+box_h-8], radius=14, outline=GOLD, width=2)
center(d, "USA EL C" + O_ACC + "DIGO", box_y + 35, F_BOLD(32), (255, 248, 230))
center(d, "LANZAMIENTO20", box_y + 80, F_MONO(70), WHITE)
center(d, "Solo los primeros 20 clientes", int(H * 0.85), F_ITAL_SERIF(26), TEXT_SOFT)
img.save('video-promo/frames-v3/08-oferta.png')
print("08-oferta OK")

# ============== 09 CIERRE ==============
img = paper(W, H)
d = ImageDraw.Draw(img)
d.line([(W//2 - 80, int(H * 0.30)), (W//2 + 80, int(H * 0.30))], fill=GOLD, width=2)
center(d, "Empieza tu pedido en", int(H * 0.33), F_ITAL_SERIF(40), TEXT_SOFT)
center(d, "kodarase.com", int(H * 0.42), F_HUGE_SERIF(110), CHARCOAL)
d.line([(W//2 - 100, int(H * 0.56)), (W//2 + 100, int(H * 0.56))], fill=GOLD, width=2)
center(d, "Env" + I_ACC + "o a todo el mundo", int(H * 0.60), F_BOLD(36), TEXT_DARK)
center(d, "Sin m" + I_ACC + "nimos  " + MIDDLE_DOT + "  Calidad premium", int(H * 0.66), F_BOLD(30), TEXT_SOFT)
center(d, "KODARASE", int(H * 0.82), F_HUGE_SERIF(64), CHARCOAL)
center(d, "P R I N T   S T U D I O", int(H * 0.87), F_REG_SERIF(28), TERRACOTTA)
img.save('video-promo/frames-v3/09-cierre.png')
print("09-cierre OK")

# ============== COMPONER VIDEO ==============
APERTURA_DUR = 2.0
PRODUCTO_DUR = 1.5
OFERTA_DUR = 4.0
CIERRE_DUR = 2.0

def clip(p, dur, fi=0.3, fo=0.3):
    c = ImageClip(p).with_duration(dur)
    return c.with_effects([vfx.CrossFadeIn(fi), vfx.CrossFadeOut(fo)])

clips = [
    clip('video-promo/frames-v3/01-apertura.png', APERTURA_DUR, 0.4, 0.4),
    clip('video-promo/frames-v3/02-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v3/03-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v3/04-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v3/05-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v3/06-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v3/07-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v3/08-oferta.png', OFERTA_DUR, 0.5, 0.3),
    clip('video-promo/frames-v3/09-cierre.png', CIERRE_DUR, 0.5, 0.3),
]
video = concatenate_videoclips(clips, method='compose')

try:
    audio = AudioFileClip('marketing/brand-video/kodarase-brand-15s.mp4')
    if audio.duration < video.duration:
        audio = audio.with_effects([AudioLoop(duration=video.duration)])
    else:
        audio = audio.subclipped(0, video.duration)
    audio = audio.with_effects([AudioFadeOut(0.5)])
    video = video.with_audio(audio)
except Exception as e:
    print(f"Sin audio: {e}")

output = 'marketing/video-promo/kodarase-promo-v3.mp4'
video.write_videofile(output, codec='libx264', audio_codec='aac', fps=FPS, preset='medium', threads=4, logger=None)
print(f"OK: {output} {os.path.getsize(output):,} bytes")
