"""
Tarjetas v3 - REDISEÑO COMPLETO:
- La K-logo ES la primera letra de "Kodara" (integrada como letra)
- Texto bien espaciado sin sobreposiciones
- Fondo descriptivo que sugiere el negocio
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random
import math

OUT_DIR = r"C:\Users\lucie\kodara-se\tarjetas"
LOGO_PATH = os.path.join(OUT_DIR, 'logo-kodara-transparent.png')

W = 1110
H = 708
MARGIN = 80

BG = (8, 14, 28)
BG_DEEP = (4, 8, 18)
ORANGE = (249, 115, 22)
ORANGE_LIGHT = (251, 146, 60)
PINK = (236, 72, 153)
PURPLE = (124, 58, 237)
WHITE = (255, 255, 255)
CREAM = (250, 245, 235)
TEXT_2 = (184, 192, 208)
TEXT_3 = (107, 118, 137)


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


def make_pattern_bg_print(w, h):
    """Fondo para Print Studio: hint de marcos/lienzos sutiles"""
    img = Image.new('RGB', (w, h), BG)
    # Gradiente sutil top-bottom
    px = img.load()
    for y in range(h):
        t = y / h
        r = int(BG[0] + (BG_DEEP[0] - BG[0]) * t)
        g = int(BG[1] + (BG_DEEP[1] - BG[1]) * t)
        b = int(BG[2] + (BG_DEEP[2] - BG[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)

    # Patron de marcos pequenos (frames) en muy baja opacidad
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    random.seed(42)
    for _ in range(40):
        x = random.randint(-20, w)
        y = random.randint(-20, h)
        fw = random.randint(30, 80)
        fh = int(fw * random.uniform(1.0, 1.4))
        # Marco rectangular
        opacity = random.randint(8, 18)
        draw.rectangle([x, y, x+fw, y+fh], outline=(255, 255, 255, opacity), width=2)

    # Gaussian blur muy ligero
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=1))
    img.paste(overlay, (0, 0), overlay)

    # Acento gradiente naranja-rosa en una esquina (sutil)
    accent = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    accent_draw = ImageDraw.Draw(accent)
    # Glow en esquina top-right
    for r in range(400, 0, -8):
        alpha = int(30 * (1 - r/400))
        if r > 200:
            color = (*ORANGE, alpha)
        else:
            color = (*PINK, alpha)
        accent_draw.ellipse([w-r, -r//2, w+r, r], fill=color)
    accent = accent.filter(ImageFilter.GaussianBlur(radius=40))
    img.paste(accent, (0, 0), accent)

    # Glow en esquina bottom-left
    accent2 = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ad = ImageDraw.Draw(accent2)
    for r in range(350, 0, -8):
        alpha = int(28 * (1 - r/350))
        color = (*PURPLE, alpha) if r > 175 else (*PINK, alpha)
        ad.ellipse([-r, h-r, r, h+r//2], fill=color)
    accent2 = accent2.filter(ImageFilter.GaussianBlur(radius=40))
    img.paste(accent2, (0, 0), accent2)

    return img


def make_pattern_bg_digital(w, h):
    """Fondo para Digital Studio: grid tech pattern"""
    img = Image.new('RGB', (w, h), BG)
    px = img.load()
    for y in range(h):
        t = y / h
        r = int(BG[0] + (BG_DEEP[0] - BG[0]) * t)
        g = int(BG[1] + (BG_DEEP[1] - BG[1]) * t)
        b = int(BG[2] + (BG_DEEP[2] - BG[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)

    # Grid pattern
    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    grid = 50
    for x in range(0, w + grid, grid):
        draw.line([(x, 0), (x, h)], fill=(255, 255, 255, 6), width=1)
    for y in range(0, h + grid, grid):
        draw.line([(0, y), (w, y)], fill=(255, 255, 255, 6), width=1)

    # Dots accent en intersecciones
    for x in range(grid, w, grid):
        for y in range(grid, h, grid):
            if random.random() < 0.08:
                draw.ellipse([x-3, y-3, x+3, y+3], fill=(*ORANGE, 80))

    img.paste(overlay, (0, 0), overlay)

    # Glow corners
    accent = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ad = ImageDraw.Draw(accent)
    for r in range(400, 0, -8):
        alpha = int(35 * (1 - r/400))
        ad.ellipse([w-r, -r, w+r, r], fill=(*PINK, alpha) if r > 200 else (*PURPLE, alpha))
    accent = accent.filter(ImageFilter.GaussianBlur(radius=45))
    img.paste(accent, (0, 0), accent)

    accent2 = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ad2 = ImageDraw.Draw(accent2)
    for r in range(350, 0, -8):
        alpha = int(35 * (1 - r/350))
        ad2.ellipse([-r, h-r, r, h+r], fill=(*ORANGE, alpha) if r > 175 else (*PINK, alpha))
    accent2 = accent2.filter(ImageFilter.GaussianBlur(radius=45))
    img.paste(accent2, (0, 0), accent2)

    return img


def paste_logo_as_letter(img, logo_x, logo_y, target_h, draw_text=None, text=None, font=None, color=WHITE):
    """Pega el logo COMO si fuera la letra K, seguido del texto.
    Devuelve el ancho total del logo+texto."""
    logo = Image.open(LOGO_PATH).convert('RGBA')
    # Escalar logo a la altura objetivo
    ratio = target_h / logo.height
    logo_w = int(logo.width * ratio)
    logo_scaled = logo.resize((logo_w, target_h), Image.LANCZOS)
    img.paste(logo_scaled, (logo_x, logo_y), logo_scaled)

    if draw_text is not None and text is not None and font is not None:
        # Posicionar texto inmediatamente despues del logo
        # El espaciado es como el "kerning" de letras
        text_x = logo_x + logo_w - 5  # ligeramente solapado para parecer una palabra
        # Bajar el texto un poco para alinear baseline con logo
        bbox = draw_text.textbbox((0, 0), text, font=font)
        text_h = bbox[3] - bbox[1]
        # Ajustar Y para que baseline coincida visualmente
        text_y = logo_y + (target_h - text_h) // 2 - 8
        draw_text.text((text_x, text_y), text, fill=color, font=font)
        bbox2 = draw_text.textbbox((text_x, text_y), text, font=font)
        return bbox2[2] - logo_x  # ancho total desde logo a fin de texto
    return logo_w


# ==========================================
# TARJETA A - KODARA PRINT (FRENTE)
# ==========================================

def make_print_front():
    img = make_pattern_bg_print(W, H)
    draw = ImageDraw.Draw(img)

    # ======= LOGO + "odara" centrado =======
    logo_h = 130
    f_brand = get_font(140, 'black')

    # Calcular ancho total
    text_rest = 'odara'
    bbox = draw.textbbox((0, 0), text_rest, font=f_brand)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    logo = Image.open(LOGO_PATH)
    logo_ratio = logo_h / logo.height
    logo_w = int(logo.width * logo_ratio)

    # El logo se solapa ligeramente con el texto (-10 px) para parecer una sola palabra
    overlap = 10
    total_w = logo_w + text_w - overlap

    # Posicion del bloque: centrado horizontal, en la parte superior-media
    block_x = (W - total_w) // 2
    block_y = 170

    # Pegar logo
    logo_y = block_y
    logo_scaled = Image.open(LOGO_PATH).convert('RGBA').resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo_scaled, (block_x, logo_y), logo_scaled)

    # Pegar texto "odara" alineado con baseline del logo
    text_x = block_x + logo_w - overlap
    # baseline alignment: la cap-height del font es ~0.7-0.75 del tamano del font
    # El logo se ve aproximadamente como una mayuscula completa
    text_y = block_y + (logo_h - text_h) // 2 - 22
    draw.text((text_x, text_y), text_rest, fill=WHITE, font=f_brand)

    # ======= LINEA SEPARADORA =======
    line_y = block_y + logo_h + 35
    line_w = 200
    draw.line([(W//2 - line_w//2, line_y), (W//2 + line_w//2, line_y)],
              fill=ORANGE, width=3)

    # ======= TAGLINE DESCRIPTIVO =======
    f_tag_big = get_font(32, 'bold')
    tag_main = 'PRINT  STUDIO'
    bbox = draw.textbbox((0, 0), tag_main, font=f_tag_big)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 18), tag_main, fill=ORANGE, font=f_tag_big)

    # ======= SERVICIOS =======
    f_serv = get_font(20, 'regular')
    serv = "Lienzos · Pósteres · Marcos · Aluminio · Plexiglás"
    bbox = draw.textbbox((0, 0), serv, font=f_serv)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 70), serv, fill=TEXT_2, font=f_serv)

    # ======= URL ABAJO =======
    f_url = get_font(24, 'bold')
    url = 'kodarase.com'
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 75), url, fill=PINK, font=f_url)

    return img


def make_print_back():
    img = make_pattern_bg_print(W, H)
    draw = ImageDraw.Draw(img)

    # ======= HEADER: mini logo + kodara print =======
    logo_h = 60
    logo = Image.open(LOGO_PATH).convert('RGBA')
    logo_w = int(logo.width * (logo_h / logo.height))
    logo_scaled = logo.resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo_scaled, (MARGIN, MARGIN), logo_scaled)

    # "odara" texto pequeno al lado
    f_smbrand = get_font(48, 'black')
    text_x = MARGIN + logo_w - 4
    text_y = MARGIN - 4
    draw.text((text_x, text_y), 'odara', fill=WHITE, font=f_smbrand)

    # "Print Studio" abajo del header
    f_studio_sm = get_font(15, 'bold')
    draw.text((MARGIN + 8, MARGIN + logo_h + 8),
              'P R I N T   S T U D I O', fill=ORANGE, font=f_studio_sm)

    # ======= DATOS CLIENTE (centrados) =======
    cy = H // 2 + 50

    # Nombre
    name = 'Angel Luis Andújar'
    f_value = get_font(38, 'bold')
    bbox = draw.textbbox((0, 0), name, font=f_value)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 95), name, fill=WHITE, font=f_value)

    # Cargo
    role = 'FOUNDER'
    f_cargo = get_font(22, 'bold')
    bbox = draw.textbbox((0, 0), role, font=f_cargo)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 38), role, fill=ORANGE, font=f_cargo)

    # Separador linea
    sep_y = cy + 5
    draw.line([(W//2 - 80, sep_y), (W//2 + 80, sep_y)], fill=PINK, width=2)

    # Email
    f_contact = get_font(24, 'regular')
    email = 'kodarase@gmail.com'
    bbox = draw.textbbox((0, 0), email, font=f_contact)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 32), email, fill=TEXT_2, font=f_contact)

    # URL
    url = 'kodarase.com'
    f_url = get_font(26, 'bold')
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 75), url, fill=PINK, font=f_url)

    return img


# ==========================================
# TARJETA B - KODARA DIGITAL (FRENTE)
# ==========================================

def make_universal_front():
    img = make_pattern_bg_digital(W, H)
    draw = ImageDraw.Draw(img)

    # ======= LOGO + "ODARA" GIGANTE (centrado en upper area) =======
    logo_h = 165
    f_brand = get_font(180, 'black')

    text_rest = 'ODARA'
    bbox = draw.textbbox((0, 0), text_rest, font=f_brand)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    logo = Image.open(LOGO_PATH)
    logo_w = int(logo.width * (logo_h / logo.height))

    overlap = 15
    total_w = logo_w + text_w - overlap
    block_x = (W - total_w) // 2
    block_y = 145

    # Pegar logo
    logo_scaled = Image.open(LOGO_PATH).convert('RGBA').resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo_scaled, (block_x, block_y), logo_scaled)

    # Texto ODARA con gradiente
    text_layer_mask = Image.new('L', (W, H), 0)
    md = ImageDraw.Draw(text_layer_mask)
    text_x = block_x + logo_w - overlap
    text_y = block_y + (logo_h - text_h) // 2 - 30
    md.text((text_x, text_y), text_rest, fill=255, font=f_brand)

    # Gradiente para el texto
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

    img.paste(grad, (0, 0), text_layer_mask)

    # Redibujamos draw
    draw = ImageDraw.Draw(img)

    # ======= LINEA + SUBTITLE =======
    line_y = block_y + logo_h + 50
    draw.line([(W//2 - 110, line_y), (W//2 + 110, line_y)], fill=ORANGE, width=3)

    f_sub = get_font(32, 'bold')
    sub = 'DIGITAL  STUDIO'
    bbox = draw.textbbox((0, 0), sub, font=f_sub)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 18), sub, fill=ORANGE, font=f_sub)

    # ======= SERVICIOS =======
    f_serv = get_font(20, 'regular')
    serv = "Web · Marketing · SEO · Automatización · Prints"
    bbox = draw.textbbox((0, 0), serv, font=f_serv)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 70), serv, fill=TEXT_2, font=f_serv)

    # URL
    f_url = get_font(24, 'bold')
    url = 'kodarase.com'
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 75), url, fill=PINK, font=f_url)

    return img


def make_universal_back():
    img = make_pattern_bg_digital(W, H)
    draw = ImageDraw.Draw(img)

    # Header
    logo_h = 60
    logo = Image.open(LOGO_PATH).convert('RGBA')
    logo_w = int(logo.width * (logo_h / logo.height))
    logo_scaled = logo.resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo_scaled, (MARGIN, MARGIN), logo_scaled)

    f_smbrand = get_font(48, 'black')
    draw.text((MARGIN + logo_w - 4, MARGIN - 4),
              'odara', fill=WHITE, font=f_smbrand)

    f_studio_sm = get_font(15, 'bold')
    draw.text((MARGIN + 8, MARGIN + logo_h + 8),
              'D I G I T A L   S T U D I O', fill=ORANGE, font=f_studio_sm)

    # Datos centrados
    cy = H // 2 + 50
    name = 'Angel Luis Andújar'
    f_value = get_font(38, 'bold')
    bbox = draw.textbbox((0, 0), name, font=f_value)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 95), name, fill=WHITE, font=f_value)

    role = 'FOUNDER'
    f_cargo = get_font(22, 'bold')
    bbox = draw.textbbox((0, 0), role, font=f_cargo)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy - 38), role, fill=ORANGE, font=f_cargo)

    sep_y = cy + 5
    draw.line([(W//2 - 80, sep_y), (W//2 + 80, sep_y)], fill=PINK, width=2)

    f_contact = get_font(24, 'regular')
    email = 'kodarase@gmail.com'
    bbox = draw.textbbox((0, 0), email, font=f_contact)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 32), email, fill=TEXT_2, font=f_contact)

    url = 'kodarase.com'
    f_url = get_font(26, 'bold')
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 75), url, fill=PINK, font=f_url)

    return img


# Generar
print("Generando tarjetas v3...")
print_front = make_print_front()
print_front.save(os.path.join(OUT_DIR, 'tarjeta-print-front-v3.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-print-front-v3.png")

print_back = make_print_back()
print_back.save(os.path.join(OUT_DIR, 'tarjeta-print-back-v3.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-print-back-v3.png")

universal_front = make_universal_front()
universal_front.save(os.path.join(OUT_DIR, 'tarjeta-universal-front-v3.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-universal-front-v3.png")

universal_back = make_universal_back()
universal_back.save(os.path.join(OUT_DIR, 'tarjeta-universal-back-v3.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-universal-back-v3.png")
print("\nDONE")
