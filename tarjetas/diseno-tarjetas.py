"""
Genera 2 tarjetas de visita Kodara (frente + reverso) a 300 DPI listas para imprimir.

Tamano: 88x54 mm con 3mm bleed (estandar Gelato/Vistaprint)
Resolution: 300 DPI -> 1110x720 px con bleed
Safe zone: 3mm inside trim

Tarjetas:
A) Kodara Print Studio - enfoque prints
B) Kodara Digital - universal (agencia + prints)
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = r"C:\Users\lucie\kodara-se\tarjetas"
os.makedirs(OUT_DIR, exist_ok=True)

# Dimensiones a 300 DPI con bleed 3mm
# 88x54mm + 3mm bleed = 94x60mm
# 94mm = 3.7 in -> 1110 px
# 60mm = 2.36 in -> 708 px
W = 1110
H = 708
SAFE_MARGIN = 75  # 6mm safe zone (3mm bleed + 3mm safe)

# Colores brand Kodara
BG = (6, 11, 24)           # bg navy
BG_2 = (10, 20, 36)        # darker
ORANGE = (249, 115, 22)    # #F97316
PINK = (236, 72, 153)      # #EC4899
PURPLE = (124, 58, 237)    # #7C3AED
WHITE = (255, 255, 255)
TEXT_2 = (184, 192, 208)   # #B8C0D0
TEXT_3 = (107, 118, 137)   # #6B7689

# Fonts - buscar en Windows
FONT_PATHS = [
    "C:/Windows/Fonts/seguibl.ttf",   # Segoe UI Black
    "C:/Windows/Fonts/segoeuib.ttf",  # Segoe UI Bold
    "C:/Windows/Fonts/segoeui.ttf",   # Segoe UI Regular
    "C:/Windows/Fonts/SegoeUI.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/calibri.ttf",
]

def get_font(size, weight='regular'):
    """Obtiene font de tamano y peso. Fallback a default."""
    if weight == 'black':
        candidates = ['seguibl.ttf', 'segoeuib.ttf', 'arialbd.ttf']
    elif weight == 'bold':
        candidates = ['segoeuib.ttf', 'arialbd.ttf']
    else:
        candidates = ['segoeui.ttf', 'SegoeUI.ttf', 'arial.ttf', 'calibri.ttf']

    for f in candidates:
        path = f"C:/Windows/Fonts/{f}"
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    # Fallback
    return ImageFont.load_default()

def make_gradient_bg(w, h, c1=BG, c2=BG_2):
    """Fondo gradiente sutil"""
    img = Image.new('RGB', (w, h), c1)
    pixels = img.load()
    for y in range(h):
        t = y / h
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        for x in range(w):
            pixels[x, y] = (r, g, b)
    return img

def add_corner_accent(img, size=200, position='top-left'):
    """Anade un acento gradiente naranja-rosa en una esquina"""
    accent = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(accent)
    # Circulo borroso con gradiente
    for r in range(size//2, 0, -2):
        alpha = int(80 * (1 - r/(size/2)))
        # Color mezcla
        if r > size/3:
            color = (*ORANGE, alpha)
        else:
            color = (*PINK, alpha)
        draw.ellipse([size//2-r, size//2-r, size//2+r, size//2+r], fill=color)
    # Blur
    accent = accent.filter(ImageFilter.GaussianBlur(radius=20))

    # Posicionar
    if position == 'top-left':
        pos = (-size//2, -size//2)
    elif position == 'bottom-right':
        pos = (img.width - size//2, img.height - size//2)
    elif position == 'top-right':
        pos = (img.width - size//2, -size//2)
    elif position == 'bottom-left':
        pos = (-size//2, img.height - size//2)
    img.paste(accent, pos, accent)
    return img


# ==========================================
# TARJETA A - KODARA PRINT STUDIO (FRENTE)
# ==========================================

def make_print_front():
    img = make_gradient_bg(W, H)
    img = add_corner_accent(img, size=600, position='top-left')
    img = add_corner_accent(img, size=500, position='bottom-right')
    draw = ImageDraw.Draw(img)

    # Logo "Kodara" grande estilizado
    f_brand = get_font(95, 'black')
    f_sub = get_font(28, 'bold')
    f_tag = get_font(22, 'regular')

    # Texto centrado
    cx, cy = W // 2, H // 2

    # "K" grande estilizada como logo
    logo_size = 110
    logo_x = cx - 240
    logo_y = cy - 70
    # Circulo gradiente para K
    draw.ellipse([logo_x, logo_y, logo_x + logo_size, logo_y + logo_size],
                 fill=ORANGE)

    # K dentro del circulo
    f_logo = get_font(72, 'black')
    bbox = draw.textbbox((0, 0), 'K', font=f_logo)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((logo_x + logo_size//2 - tw//2, logo_y + logo_size//2 - th//2 - 8),
              'K', fill=WHITE, font=f_logo)

    # "Kodara" texto
    draw.text((logo_x + logo_size + 25, cy - 50),
              'Kodara', fill=WHITE, font=f_brand)

    # "PRINT STUDIO" debajo
    f_studio = get_font(26, 'bold')
    draw.text((logo_x + logo_size + 28, cy + 35),
              'PRINT  STUDIO', fill=ORANGE, font=f_studio)

    # Tagline abajo
    f_tagline = get_font(20, 'regular')
    tagline = "Lienzos · Pósteres · Marcos · Aluminio · Plexiglás"
    bbox = draw.textbbox((0, 0), tagline, font=f_tagline)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 130), tagline, fill=TEXT_2, font=f_tagline)

    # URL abajo
    f_url = get_font(22, 'bold')
    url = 'kodarase.com'
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 85), url, fill=PINK, font=f_url)

    return img


def make_print_back():
    """Reverso tarjeta Print - datos de contacto"""
    img = make_gradient_bg(W, H)
    img = add_corner_accent(img, size=500, position='top-right')
    img = add_corner_accent(img, size=400, position='bottom-left')
    draw = ImageDraw.Draw(img)

    # Top barra accent
    f_label = get_font(20, 'bold')
    f_value = get_font(30, 'bold')
    f_role = get_font(22, 'regular')

    # Mini logo top
    logo_size = 60
    draw.ellipse([SAFE_MARGIN, SAFE_MARGIN, SAFE_MARGIN + logo_size, SAFE_MARGIN + logo_size],
                 fill=ORANGE)
    f_logo_mini = get_font(38, 'black')
    bbox = draw.textbbox((0, 0), 'K', font=f_logo_mini)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((SAFE_MARGIN + logo_size//2 - tw//2, SAFE_MARGIN + logo_size//2 - th//2 - 5),
              'K', fill=WHITE, font=f_logo_mini)
    # "Kodara Print" small
    f_smbrand = get_font(26, 'black')
    draw.text((SAFE_MARGIN + logo_size + 18, SAFE_MARGIN + 12),
              'Kodara Print', fill=WHITE, font=f_smbrand)

    # Datos del cliente (centrados)
    cx, cy = W // 2, H // 2 + 30

    # Nombre
    name = 'Angel Luis Andújar'
    bbox = draw.textbbox((0, 0), name, font=f_value)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 80), name, fill=WHITE, font=f_value)

    # Cargo
    role = 'Founder'
    f_cargo = get_font(20, 'bold')
    bbox = draw.textbbox((0, 0), role, font=f_cargo)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 36), role.upper(), fill=ORANGE, font=f_cargo)

    # Separador linea
    sep_y = cy + 5
    draw.line([(W//2 - 60, sep_y), (W//2 + 60, sep_y)], fill=PINK, width=2)

    # Email
    f_contact = get_font(22, 'regular')
    email = 'kodarase@gmail.com'
    bbox = draw.textbbox((0, 0), email, font=f_contact)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 30), email, fill=TEXT_2, font=f_contact)

    # URL
    url = 'kodarase.com'
    f_url = get_font(24, 'bold')
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 70), url, fill=PINK, font=f_url)

    return img


# ==========================================
# TARJETA B - KODARA UNIVERSAL (agencia + prints)
# ==========================================

def make_universal_front():
    """Frente tarjeta universal - solo brand"""
    img = make_gradient_bg(W, H)
    img = add_corner_accent(img, size=700, position='bottom-right')
    img = add_corner_accent(img, size=400, position='top-left')
    draw = ImageDraw.Draw(img)

    # KODARA gigante centrado
    f_giant = get_font(160, 'black')
    text = 'KODARA'
    bbox = draw.textbbox((0, 0), text, font=f_giant)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    text_x = (W - tw) // 2
    text_y = (H - th) // 2 - 30

    # Crear un layer con el texto en gradiente
    text_layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    text_mask = Image.new('L', (W, H), 0)
    mask_draw = ImageDraw.Draw(text_mask)
    mask_draw.text((text_x, text_y), text, fill=255, font=f_giant)

    # Gradiente orange -> pink -> purple
    grad = Image.new('RGB', (W, H), ORANGE)
    grad_px = grad.load()
    for x in range(W):
        t = x / W
        if t < 0.5:
            tt = t * 2
            r = int(ORANGE[0] + (PINK[0] - ORANGE[0]) * tt)
            g = int(ORANGE[1] + (PINK[1] - ORANGE[1]) * tt)
            b = int(ORANGE[2] + (PINK[2] - ORANGE[2]) * tt)
        else:
            tt = (t - 0.5) * 2
            r = int(PINK[0] + (PURPLE[0] - PINK[0]) * tt)
            g = int(PINK[1] + (PURPLE[1] - PINK[1]) * tt)
            b = int(PINK[2] + (PURPLE[2] - PINK[2]) * tt)
        for y in range(H):
            grad_px[x, y] = (r, g, b)

    # Aplicar mascara
    img.paste(grad, (0, 0), text_mask)

    # Tagline abajo
    draw = ImageDraw.Draw(img)
    f_tag = get_font(22, 'bold')
    tagline = 'DIGITAL  STUDIO'
    bbox = draw.textbbox((0, 0), tagline, font=f_tag)
    tw = bbox[2] - bbox[0]
    tagline_y = text_y + th + 30
    draw.text(((W - tw) // 2, tagline_y), tagline, fill=TEXT_2, font=f_tag)

    # Servicios pequenos
    f_serv = get_font(16, 'regular')
    serv = 'Web · Marketing · SEO · Prints · Automatización'
    bbox = draw.textbbox((0, 0), serv, font=f_serv)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 80), serv, fill=TEXT_3, font=f_serv)

    return img


def make_universal_back():
    """Reverso tarjeta universal"""
    img = make_gradient_bg(W, H)
    img = add_corner_accent(img, size=500, position='top-left')
    img = add_corner_accent(img, size=400, position='bottom-right')
    draw = ImageDraw.Draw(img)

    # Mini logo + brand top
    logo_size = 60
    draw.ellipse([SAFE_MARGIN, SAFE_MARGIN, SAFE_MARGIN + logo_size, SAFE_MARGIN + logo_size],
                 fill=ORANGE)
    f_logo_mini = get_font(38, 'black')
    bbox = draw.textbbox((0, 0), 'K', font=f_logo_mini)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((SAFE_MARGIN + logo_size//2 - tw//2, SAFE_MARGIN + logo_size//2 - th//2 - 5),
              'K', fill=WHITE, font=f_logo_mini)
    f_smbrand = get_font(26, 'black')
    draw.text((SAFE_MARGIN + logo_size + 18, SAFE_MARGIN + 12),
              'Kodara', fill=WHITE, font=f_smbrand)
    f_studio = get_font(15, 'bold')
    draw.text((SAFE_MARGIN + logo_size + 18, SAFE_MARGIN + 45),
              'DIGITAL  STUDIO', fill=ORANGE, font=f_studio)

    # Datos centrados
    cx, cy = W // 2, H // 2 + 30

    # Nombre
    name = 'Angel Luis Andújar'
    f_name = get_font(32, 'bold')
    bbox = draw.textbbox((0, 0), name, font=f_name)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 80), name, fill=WHITE, font=f_name)

    # Cargo
    role = 'FOUNDER'
    f_cargo = get_font(20, 'bold')
    bbox = draw.textbbox((0, 0), role, font=f_cargo)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 36), role, fill=ORANGE, font=f_cargo)

    # Separador
    sep_y = cy + 5
    draw.line([(W//2 - 60, sep_y), (W//2 + 60, sep_y)], fill=PINK, width=2)

    # Email
    f_contact = get_font(22, 'regular')
    email = 'kodarase@gmail.com'
    bbox = draw.textbbox((0, 0), email, font=f_contact)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 30), email, fill=TEXT_2, font=f_contact)

    # URL
    url = 'kodarase.com'
    f_url = get_font(24, 'bold')
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 70), url, fill=PINK, font=f_url)

    return img


# ==========================================
# RENDER ALL
# ==========================================

print("Generando tarjetas...\n")

print_front = make_print_front()
print_front.save(os.path.join(OUT_DIR, 'tarjeta-print-front.png'), 'PNG', dpi=(300, 300))
print(f"OK tarjeta-print-front.png ({print_front.size})")

print_back = make_print_back()
print_back.save(os.path.join(OUT_DIR, 'tarjeta-print-back.png'), 'PNG', dpi=(300, 300))
print(f"OK tarjeta-print-back.png ({print_back.size})")

universal_front = make_universal_front()
universal_front.save(os.path.join(OUT_DIR, 'tarjeta-universal-front.png'), 'PNG', dpi=(300, 300))
print(f"OK tarjeta-universal-front.png ({universal_front.size})")

universal_back = make_universal_back()
universal_back.save(os.path.join(OUT_DIR, 'tarjeta-universal-back.png'), 'PNG', dpi=(300, 300))
print(f"OK tarjeta-universal-back.png ({universal_back.size})")

print(f"\nTodas en: {OUT_DIR}")
print(f"Tamano: 88x54 mm + 3mm bleed -> 1110x708 px @ 300 DPI")
