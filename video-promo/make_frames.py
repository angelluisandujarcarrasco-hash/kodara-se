"""Genera frames del video promo."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, random

W, H = 1080, 1920

CREAM = (245, 239, 230)
CHARCOAL = (30, 25, 22)
GOLD = (201, 168, 76)
TERRACOTTA = (198, 107, 61)
TEXT_DARK = (45, 38, 32)
TEXT_SOFT = (90, 80, 68)
WHITE = (255, 253, 248)

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

F_HUGE = lambda s: font('C:/Windows/Fonts/georgiab.ttf', s)
F_ITAL = lambda s: font('C:/Windows/Fonts/georgiai.ttf', s)
F_REG  = lambda s: font('C:/Windows/Fonts/georgia.ttf', s)
F_MONO = lambda s: font('C:/Windows/Fonts/consolab.ttf', s)

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

def center(draw, text, y, fnt, color, width=W):
    bbox = draw.textbbox((0,0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, y), text, font=fnt, fill=color)

os.makedirs('video-promo/frames', exist_ok=True)

# 1. APERTURA
img = paper(W, H)
d = ImageDraw.Draw(img)
d.line([(W//2 - 80, 700), (W//2 + 80, 700)], fill=GOLD, width=2)
center(d, "PRESENTA", 740, F_REG(28), TEXT_SOFT)
center(d, "KODARASE", int(H * 0.43), F_HUGE(160), CHARCOAL)
center(d, "P R I N T   S T U D I O", int(H * 0.55), F_REG(48), TERRACOTTA)
d.line([(W//2 - 80, int(H * 0.62)), (W//2 + 80, int(H * 0.62))], fill=GOLD, width=2)
center(d, "Tus recuerdos hechos arte", int(H * 0.65), F_ITAL(36), TEXT_SOFT)
img.save('video-promo/frames/01-apertura.png')
print('01-apertura OK')

# 2-6 POSTERS
posters = [
    'disenos-posters/poster-01.png',
    'disenos-posters/poster-02.png',
    'disenos-posters/poster-03.png',
    'disenos-posters/poster-04.png',
    'disenos-posters/poster-05.png',
]
for i, pf in enumerate(posters, start=2):
    bg = paper(W, H, base=(238, 230, 218))
    bg_rgba = bg.convert('RGBA')
    p = Image.open(pf).convert('RGBA')
    target_h = int(H * 0.62)
    target_w = int(target_h * 2/3)
    p = p.resize((target_w, target_h), Image.LANCZOS)
    shadow = Image.new('RGBA', (target_w + 60, target_h + 60), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle([20, 30, target_w + 30, target_h + 50], fill=(0, 0, 0, 90))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=20))
    px = (W - target_w) // 2
    py = int(H * 0.18)
    bg_rgba.paste(shadow, (px - 30, py - 15), shadow)
    bg_rgba.paste(p, (px, py), p)
    dd = ImageDraw.Draw(bg_rgba)
    dd.rectangle([px-2, py-2, px+target_w+2, py+target_h+2], outline=GOLD, width=2)
    dd.line([(W//2 - 40, py + target_h + 30), (W//2 + 40, py + target_h + 30)], fill=GOLD, width=2)
    bg_rgba.convert('RGB').save(f'video-promo/frames/0{i}-poster.png')
    print(f'0{i}-poster OK')

# 7. OFERTA
img = paper(W, H)
d = ImageDraw.Draw(img)
center(d, "PRIMERA COMPRA", int(H * 0.20), F_REG(38), TERRACOTTA)
center(d, "20% OFF", int(H * 0.27), F_HUGE(220), CHARCOAL)
d.line([(W//2 - 120, int(H * 0.50)), (W//2 + 120, int(H * 0.50))], fill=GOLD, width=2)
center(d, "tu primer pedido", int(H * 0.52), F_ITAL(42), TEXT_SOFT)
box_w, box_h = 720, 180
box_x = (W - box_w) // 2
box_y = int(H * 0.62)
d.rounded_rectangle([box_x, box_y, box_x+box_w, box_y+box_h], radius=20, fill=TERRACOTTA)
d.rounded_rectangle([box_x+8, box_y+8, box_x+box_w-8, box_y+box_h-8], radius=14, outline=GOLD, width=2)
center(d, "USA EL CÓDIGO", box_y + 35, F_REG(28), (255, 248, 230))
center(d, "LANZAMIENTO20", box_y + 80, F_MONO(70), WHITE)
center(d, "Solo los primeros 20 clientes", int(H * 0.85), F_ITAL(26), TEXT_SOFT)
img.save('video-promo/frames/07-oferta.png')
print('07-oferta OK')

# 8. CIERRE
img = paper(W, H)
d = ImageDraw.Draw(img)
d.line([(W//2 - 80, int(H * 0.30)), (W//2 + 80, int(H * 0.30))], fill=GOLD, width=2)
center(d, "Empieza tu pedido en", int(H * 0.33), F_ITAL(40), TEXT_SOFT)
center(d, "kodarase.com", int(H * 0.42), F_HUGE(110), CHARCOAL)
d.line([(W//2 - 100, int(H * 0.56)), (W//2 + 100, int(H * 0.56))], fill=GOLD, width=2)
center(d, "Envío a todo el mundo", int(H * 0.60), F_REG(36), TEXT_DARK)
center(d, "Sin mínimos  ·  Calidad premium", int(H * 0.66), F_REG(30), TEXT_SOFT)
center(d, "KODARASE", int(H * 0.82), F_HUGE(64), CHARCOAL)
center(d, "P R I N T   S T U D I O", int(H * 0.87), F_REG(28), TERRACOTTA)
img.save('video-promo/frames/08-cierre.png')
print('08-cierre OK')

print('---DONE---')
for f in sorted(os.listdir('video-promo/frames')):
    p = f'video-promo/frames/{f}'
    print(f'  {f}: {os.path.getsize(p):,} bytes')
