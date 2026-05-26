"""
Tarjetas v2: usa el LOGO ORIGINAL (logo-kodara.jpeg) con fondo transparente,
y mejor alineacion del texto.
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

KODARA_DIR = r"C:\Users\lucie\kodara-se"
OUT_DIR = r"C:\Users\lucie\kodara-se\tarjetas"

W = 1110
H = 708
SAFE_MARGIN = 75

BG = (6, 11, 24)
BG_2 = (10, 20, 36)
ORANGE = (249, 115, 22)
PINK = (236, 72, 153)
PURPLE = (124, 58, 237)
WHITE = (255, 255, 255)
TEXT_2 = (184, 192, 208)
TEXT_3 = (107, 118, 137)

# ===== Procesar logo: hacer fondo blanco transparente =====
print("Procesando logo original...")
logo_src = Image.open(os.path.join(KODARA_DIR, 'logo-kodara.jpeg')).convert('RGBA')
logo_arr = np.array(logo_src)

# Detectar pixeles claros (cercanos a blanco) y hacerlos transparentes
# El fondo del logo es blanco/crema claro (~230+)
rgb = logo_arr[:, :, :3]
brightness = rgb.mean(axis=2)
# Pixeles con brightness > 220 son fondo
mask_bg = brightness > 220
# Hacer transparente
logo_arr[mask_bg, 3] = 0

logo_transparent = Image.fromarray(logo_arr, 'RGBA')
logo_transparent.save(os.path.join(OUT_DIR, 'logo-kodara-transparent.png'))
print(f"OK logo transparente {logo_transparent.size}")


def get_font(size, weight='regular'):
    if weight == 'black':
        candidates = ['seguibl.ttf', 'segoeuib.ttf', 'arialbd.ttf']
    elif weight == 'bold':
        candidates = ['segoeuib.ttf', 'arialbd.ttf']
    else:
        candidates = ['segoeui.ttf', 'arial.ttf']
    for f in candidates:
        path = f"C:/Windows/Fonts/{f}"
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_gradient_bg(w, h, c1=BG, c2=BG_2):
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
    accent = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(accent)
    for r in range(size//2, 0, -2):
        alpha = int(80 * (1 - r/(size/2)))
        if r > size/3:
            color = (*ORANGE, alpha)
        else:
            color = (*PINK, alpha)
        draw.ellipse([size//2-r, size//2-r, size//2+r, size//2+r], fill=color)
    accent = accent.filter(ImageFilter.GaussianBlur(radius=20))
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


def paste_logo(img, x, y, target_h):
    """Pega el logo original escalado a una altura especifica."""
    logo = Image.open(os.path.join(OUT_DIR, 'logo-kodara-transparent.png')).convert('RGBA')
    # Escalar
    ratio = target_h / logo.height
    new_w = int(logo.width * ratio)
    new_h = target_h
    logo_scaled = logo.resize((new_w, new_h), Image.LANCZOS)
    img.paste(logo_scaled, (x, y), logo_scaled)
    return new_w, new_h


# ==========================================
# TARJETA A - KODARA PRINT STUDIO (FRENTE)
# ==========================================

def make_print_front():
    img = make_gradient_bg(W, H)
    img = add_corner_accent(img, size=550, position='top-left')
    img = add_corner_accent(img, size=450, position='bottom-right')
    draw = ImageDraw.Draw(img)

    # Configuracion textos
    f_brand = get_font(105, 'black')
    f_sub = get_font(28, 'bold')

    # Logo + Kodara: alineados horizontalmente, centrados verticalmente
    cy = H // 2

    # Calcular ancho total: logo + gap + texto
    logo_h = 120
    gap = 30
    # Para calcular ancho del logo escalado, lo cargamos
    logo = Image.open(os.path.join(OUT_DIR, 'logo-kodara-transparent.png'))
    logo_w = int(logo.width * (logo_h / logo.height))

    text = 'Kodara'
    bbox = draw.textbbox((0, 0), text, font=f_brand)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    total_w = logo_w + gap + text_w
    start_x = (W - total_w) // 2

    # Posicionar logo
    logo_x = start_x
    logo_y = cy - logo_h // 2 - 20
    paste_logo(img, logo_x, logo_y, logo_h)

    # Posicionar texto "Kodara"
    text_x = logo_x + logo_w + gap
    text_y = cy - text_h // 2 - 30  # ajustar para alinear con logo
    draw.text((text_x, text_y), text, fill=WHITE, font=f_brand)

    # "PRINT STUDIO" debajo del texto Kodara
    f_studio = get_font(28, 'bold')
    studio_text = 'PRINT  STUDIO'
    sb = draw.textbbox((0, 0), studio_text, font=f_studio)
    sw = sb[2] - sb[0]
    # Alinear con texto Kodara, no centro
    draw.text((text_x + 6, text_y + text_h + 18),
              studio_text, fill=ORANGE, font=f_studio)

    # Tagline abajo - servicios
    f_tagline = get_font(20, 'regular')
    tagline = "Lienzos · Pósteres · Marcos · Aluminio · Plexiglás"
    tb = draw.textbbox((0, 0), tagline, font=f_tagline)
    tw = tb[2] - tb[0]
    draw.text(((W - tw) // 2, H - 130), tagline, fill=TEXT_2, font=f_tagline)

    # URL abajo
    f_url = get_font(24, 'bold')
    url = 'kodarase.com'
    ub = draw.textbbox((0, 0), url, font=f_url)
    uw = ub[2] - ub[0]
    draw.text(((W - uw) // 2, H - 90), url, fill=PINK, font=f_url)

    return img


def make_print_back():
    img = make_gradient_bg(W, H)
    img = add_corner_accent(img, size=450, position='top-right')
    img = add_corner_accent(img, size=400, position='bottom-left')
    draw = ImageDraw.Draw(img)

    # Mini logo + brand top
    logo_h = 70
    logo = Image.open(os.path.join(OUT_DIR, 'logo-kodara-transparent.png'))
    logo_w = int(logo.width * (logo_h / logo.height))
    paste_logo(img, SAFE_MARGIN, SAFE_MARGIN, logo_h)

    # "Kodara Print" al lado del logo
    f_smbrand = get_font(28, 'black')
    draw.text((SAFE_MARGIN + logo_w + 16, SAFE_MARGIN + 12),
              'Kodara Print', fill=WHITE, font=f_smbrand)
    f_studio_sm = get_font(15, 'bold')
    draw.text((SAFE_MARGIN + logo_w + 16, SAFE_MARGIN + 45),
              'PRINT  STUDIO', fill=ORANGE, font=f_studio_sm)

    # Datos del cliente (centrados)
    cx, cy = W // 2, H // 2 + 30

    # Nombre
    name = 'Angel Luis Andújar'
    f_value = get_font(34, 'bold')
    bbox = draw.textbbox((0, 0), name, font=f_value)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 80), name, fill=WHITE, font=f_value)

    # Cargo
    role = 'FOUNDER'
    f_cargo = get_font(20, 'bold')
    bbox = draw.textbbox((0, 0), role, font=f_cargo)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 32), role, fill=ORANGE, font=f_cargo)

    # Separador
    sep_y = cy + 8
    draw.line([(W//2 - 70, sep_y), (W//2 + 70, sep_y)], fill=PINK, width=2)

    # Email
    f_contact = get_font(22, 'regular')
    email = 'kodarase@gmail.com'
    bbox = draw.textbbox((0, 0), email, font=f_contact)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 30), email, fill=TEXT_2, font=f_contact)

    # URL
    url = 'kodarase.com'
    f_url = get_font(26, 'bold')
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 72), url, fill=PINK, font=f_url)

    return img


# ==========================================
# TARJETA B - KODARA UNIVERSAL (FRENTE)
# ==========================================

def make_universal_front():
    img = make_gradient_bg(W, H)
    img = add_corner_accent(img, size=600, position='bottom-right')
    img = add_corner_accent(img, size=350, position='top-left')
    draw = ImageDraw.Draw(img)

    # LOGO grande + KODARA grande al lado
    f_giant = get_font(140, 'black')
    text = 'KODARA'
    bbox = draw.textbbox((0, 0), text, font=f_giant)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # Logo a la izquierda
    logo_h = 160
    logo = Image.open(os.path.join(OUT_DIR, 'logo-kodara-transparent.png'))
    logo_w = int(logo.width * (logo_h / logo.height))
    gap = 25

    total_w = logo_w + gap + text_w
    start_x = (W - total_w) // 2
    cy = H // 2 - 20

    logo_x = start_x
    logo_y = cy - logo_h // 2
    paste_logo(img, logo_x, logo_y, logo_h)

    # Texto KODARA con gradient
    text_x = logo_x + logo_w + gap
    text_y = cy - text_h // 2 - 18

    # Hacer gradient text mascara
    text_mask = Image.new('L', (W, H), 0)
    mask_draw = ImageDraw.Draw(text_mask)
    mask_draw.text((text_x, text_y), text, fill=255, font=f_giant)

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

    img.paste(grad, (0, 0), text_mask)

    # Re-draw porque pegamos un nuevo Image
    draw = ImageDraw.Draw(img)

    # Tagline debajo
    f_tag = get_font(22, 'bold')
    tagline = 'DIGITAL  STUDIO'
    bbox = draw.textbbox((0, 0), tagline, font=f_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + text_h // 2 + 20), tagline, fill=TEXT_2, font=f_tag)

    # Servicios
    f_serv = get_font(16, 'regular')
    serv = 'Web · Marketing · SEO · Prints · Automatización'
    bbox = draw.textbbox((0, 0), serv, font=f_serv)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 75), serv, fill=TEXT_3, font=f_serv)

    return img


def make_universal_back():
    img = make_gradient_bg(W, H)
    img = add_corner_accent(img, size=450, position='top-left')
    img = add_corner_accent(img, size=400, position='bottom-right')
    draw = ImageDraw.Draw(img)

    # Mini logo top
    logo_h = 70
    logo = Image.open(os.path.join(OUT_DIR, 'logo-kodara-transparent.png'))
    logo_w = int(logo.width * (logo_h / logo.height))
    paste_logo(img, SAFE_MARGIN, SAFE_MARGIN, logo_h)

    f_smbrand = get_font(28, 'black')
    draw.text((SAFE_MARGIN + logo_w + 16, SAFE_MARGIN + 12),
              'Kodara', fill=WHITE, font=f_smbrand)
    f_studio_sm = get_font(15, 'bold')
    draw.text((SAFE_MARGIN + logo_w + 16, SAFE_MARGIN + 45),
              'DIGITAL  STUDIO', fill=ORANGE, font=f_studio_sm)

    # Datos centrados
    cy = H // 2 + 30

    name = 'Angel Luis Andújar'
    f_name = get_font(34, 'bold')
    bbox = draw.textbbox((0, 0), name, font=f_name)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 80), name, fill=WHITE, font=f_name)

    role = 'FOUNDER'
    f_cargo = get_font(20, 'bold')
    bbox = draw.textbbox((0, 0), role, font=f_cargo)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 32), role, fill=ORANGE, font=f_cargo)

    sep_y = cy + 8
    draw.line([(W//2 - 70, sep_y), (W//2 + 70, sep_y)], fill=PINK, width=2)

    f_contact = get_font(22, 'regular')
    email = 'kodarase@gmail.com'
    bbox = draw.textbbox((0, 0), email, font=f_contact)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 30), email, fill=TEXT_2, font=f_contact)

    url = 'kodarase.com'
    f_url = get_font(26, 'bold')
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 72), url, fill=PINK, font=f_url)

    return img


# Generar
print("\nGenerando tarjetas v2...")

print_front = make_print_front()
print_front.save(os.path.join(OUT_DIR, 'tarjeta-print-front-v2.png'), 'PNG', dpi=(300, 300))
print(f"OK tarjeta-print-front-v2.png")

print_back = make_print_back()
print_back.save(os.path.join(OUT_DIR, 'tarjeta-print-back-v2.png'), 'PNG', dpi=(300, 300))
print(f"OK tarjeta-print-back-v2.png")

universal_front = make_universal_front()
universal_front.save(os.path.join(OUT_DIR, 'tarjeta-universal-front-v2.png'), 'PNG', dpi=(300, 300))
print(f"OK tarjeta-universal-front-v2.png")

universal_back = make_universal_back()
universal_back.save(os.path.join(OUT_DIR, 'tarjeta-universal-back-v2.png'), 'PNG', dpi=(300, 300))
print(f"OK tarjeta-universal-back-v2.png")

print(f"\nTodas en: {OUT_DIR}")
