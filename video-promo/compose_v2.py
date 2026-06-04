"""Video promo v2 — con productos Higgsfield + apertura/oferta/cierre del v1."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips, vfx
from moviepy.audio.fx import AudioFadeOut, AudioLoop
import os, random

W, H = 1080, 1920
FPS = 30

CREAM = (245, 239, 230)
CHARCOAL = (30, 25, 22)
GOLD = (201, 168, 76)
TERRACOTTA = (198, 107, 61)
WHITE = (255, 253, 248)
TEXT_DARK = (45, 38, 32)
TEXT_SOFT = (90, 80, 68)

def font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

F_HUGE = lambda s: font('C:/Windows/Fonts/georgiab.ttf', s)
F_ITAL = lambda s: font('C:/Windows/Fonts/georgiai.ttf', s)
F_REG  = lambda s: font('C:/Windows/Fonts/georgia.ttf', s)
F_SANS = lambda s: font('C:/Windows/Fonts/arialbd.ttf', s)

def center(d, text, y, fnt, color, w=W):
    bbox = d.textbbox((0,0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    d.text(((w - tw) // 2, y), text, font=fnt, fill=color)

def make_product_frame(prod_img_path, label, sublabel=''):
    """Frame del producto: imagen Higgsfield fullscreen + banner inferior con titulo."""
    # Cargar imagen producto
    prod = Image.open(prod_img_path).convert('RGB')
    # Escalar y croppear a 1080x1920
    src_w, src_h = prod.size
    src_ratio = src_w / src_h
    tgt_ratio = W / H
    if src_ratio > tgt_ratio:
        # source mas ancha, cropear lados
        new_w = int(src_h * tgt_ratio)
        offset = (src_w - new_w) // 2
        prod = prod.crop((offset, 0, offset + new_w, src_h))
    else:
        new_h = int(src_w / tgt_ratio)
        offset = (src_h - new_h) // 2
        prod = prod.crop((0, offset, src_w, offset + new_h))
    prod = prod.resize((W, H), Image.LANCZOS)

    # Banner inferior semi-transparente
    overlay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    # Gradient oscuro en la parte inferior
    for y in range(int(H * 0.78), H):
        progress = (y - int(H*0.78)) / (H - int(H*0.78))
        alpha = int(180 * progress ** 1.2)
        od.line([(0, y), (W, y)], fill=(20, 14, 10, alpha))

    img = Image.alpha_composite(prod.convert('RGBA'), overlay).convert('RGB')
    d = ImageDraw.Draw(img)

    # Linea dorada decorativa
    d.line([(W//2 - 60, int(H * 0.83)), (W//2 + 60, int(H * 0.83))], fill=GOLD, width=2)
    # Label producto
    center(d, label, int(H * 0.86), F_HUGE(72), WHITE)
    # Sublabel
    if sublabel:
        center(d, sublabel, int(H * 0.93), F_ITAL(34), (220, 210, 195))

    return img

# Generar frames de productos
products = [
    ('video-promo/productos-higgsfield/01-lienzo-enmarcado.png', 'Lienzos Enmarcados', 'Madera natural · 13 tamaños'),
    ('video-promo/productos-higgsfield/02-marco-madera.png', 'Marcos de Madera', 'Roble premium · 22 tamaños'),
    ('video-promo/productos-higgsfield/03-aluminio.png', 'Impresión en Aluminio', 'Metálico moderno · 18 tamaños'),
    ('video-promo/productos-higgsfield/04-plexiglas.png', 'Plexiglás Brillante', 'Cristal acrílico · 18 tamaños'),
    ('video-promo/productos-higgsfield/05-madera.png', 'Impresión en Madera', 'Roble rústico · 18 tamaños'),
    ('video-promo/productos-higgsfield/06-espuma.png', 'Panel de Espuma', 'Ligero · 13 tamaños'),
]

os.makedirs('video-promo/frames-v2', exist_ok=True)
for i, (pf, label, sub) in enumerate(products, start=2):
    img = make_product_frame(pf, label, sub)
    img.save(f'video-promo/frames-v2/0{i}-producto.png')
    print(f'0{i}: {label} OK')

# Copiar apertura, oferta, cierre del v1
import shutil
shutil.copy('video-promo/frames/01-apertura.png', 'video-promo/frames-v2/01-apertura.png')
shutil.copy('video-promo/frames/07-oferta.png', 'video-promo/frames-v2/08-oferta.png')
shutil.copy('video-promo/frames/08-cierre.png', 'video-promo/frames-v2/09-cierre.png')
print('Apertura, oferta, cierre copiados del v1')

# Componer video
APERTURA_DUR = 2.0
PRODUCTO_DUR = 1.5
OFERTA_DUR = 4.0
CIERRE_DUR = 2.0

def clip(p, dur, fi=0.3, fo=0.3):
    c = ImageClip(p).with_duration(dur)
    return c.with_effects([vfx.CrossFadeIn(fi), vfx.CrossFadeOut(fo)])

clips = [
    clip('video-promo/frames-v2/01-apertura.png', APERTURA_DUR, 0.4, 0.4),
    clip('video-promo/frames-v2/02-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v2/03-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v2/04-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v2/05-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v2/06-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v2/07-producto.png', PRODUCTO_DUR),
    clip('video-promo/frames-v2/08-oferta.png', OFERTA_DUR, 0.5, 0.3),
    clip('video-promo/frames-v2/09-cierre.png', CIERRE_DUR, 0.5, 0.3),
]
video = concatenate_videoclips(clips, method='compose')
print(f'Duracion total: {video.duration}s')

# Audio
try:
    audio = AudioFileClip('marketing/brand-video/kodarase-brand-15s.mp4')
    if audio.duration < video.duration:
        audio = audio.with_effects([AudioLoop(duration=video.duration)])
    else:
        audio = audio.subclipped(0, video.duration)
    audio = audio.with_effects([AudioFadeOut(0.5)])
    video = video.with_audio(audio)
    print('Audio agregado')
except Exception as e:
    print(f'Sin audio: {e}')

output = 'marketing/video-promo/kodarase-promo-productos-v2.mp4'
print('Renderizando...')
video.write_videofile(
    output,
    codec='libx264',
    audio_codec='aac',
    fps=FPS,
    preset='medium',
    threads=4,
    logger=None,
)
print(f'OK: {output}')
print(f'Tamano: {os.path.getsize(output):,} bytes')
