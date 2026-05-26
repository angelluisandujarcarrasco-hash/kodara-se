"""
Tarjetas v4 - CORREGIDO:
- Nombre completo: "Kodarase" (K-logo + "odarase")
- "odarase" en BLANCO (sin gradient)
- K mejor alineada con baseline del texto
- Background con productos (collage publicitario)
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
import random

OUT_DIR = r"C:\Users\lucie\kodara-se\tarjetas"
LOGO_PATH = os.path.join(OUT_DIR, 'logo-kodara-transparent.png')
KODARA_DIR = r"C:\Users\lucie\kodara-se"

W = 1110
H = 708
MARGIN = 80

BG = (8, 14, 28)
BG_DEEP = (4, 8, 18)
ORANGE = (249, 115, 22)
PINK = (236, 72, 153)
PURPLE = (124, 58, 237)
WHITE = (255, 255, 255)
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


def make_product_bg(w, h):
    """Fondo de productos: usa imagenes reales de productos de kodarase
    como mosaic suave en muy baja opacidad."""
    img = Image.new('RGB', (w, h), BG)
    # Gradient base
    px = img.load()
    for y in range(h):
        t = y / h
        r = int(BG[0] + (BG_DEEP[0] - BG[0]) * t)
        g = int(BG[1] + (BG_DEEP[1] - BG[1]) * t)
        b = int(BG[2] + (BG_DEEP[2] - BG[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)

    # Buscar imagenes de productos en kodara-se
    product_imgs = []
    # Las imagenes locales de productos que existen
    candidates = [
        # Lienzos
        os.path.join(KODARA_DIR, 'tarjetas', 'logo-kodara-transparent.png'),
    ]

    # En vez de imagenes locales (que pueden no existir), dibujo mockups de productos
    # como siluetas/iconos en background

    overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    random.seed(7)

    # Dibujar marcos de fotos (rectangulos con borde)
    frame_color = (255, 255, 255, 14)
    for _ in range(15):
        x = random.randint(-30, w)
        y = random.randint(-30, h)
        fw = random.randint(80, 160)
        fh = int(fw * random.uniform(0.7, 1.5))
        draw.rectangle([x, y, x+fw, y+fh], outline=frame_color, width=2)
        # Mini imagen dentro del marco
        inner_color = (255, 255, 255, 6)
        draw.rectangle([x+10, y+10, x+fw-10, y+fh-10], fill=inner_color)

    # Dibujar tazas (circulos)
    cup_color = (255, 255, 255, 12)
    for _ in range(6):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.randint(50, 80)
        draw.ellipse([x, y, x+s, y+s], outline=cup_color, width=2)
        # asa
        draw.arc([x+s-10, y+10, x+s+15, y+s-10], 270, 90, fill=cup_color, width=2)

    # Dibujar camisetas (T-shirt silhouettes)
    tshirt_color = (255, 255, 255, 11)
    for _ in range(5):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.randint(60, 100)
        # T-shirt simple shape
        # cuerpo
        body = [(x+s//4, y+s//4), (x+3*s//4, y+s//4),
                (x+3*s//4, y+s),    (x+s//4, y+s)]
        draw.polygon(body, outline=tshirt_color, width=2)
        # mangas
        draw.polygon([(x, y+s//4), (x+s//4, y+s//4), (x+s//4, y+s//2), (x, y+s//2)],
                     outline=tshirt_color, width=2)
        draw.polygon([(x+3*s//4, y+s//4), (x+s, y+s//4), (x+s, y+s//2), (x+3*s//4, y+s//2)],
                     outline=tshirt_color, width=2)

    # Tote bags
    bag_color = (255, 255, 255, 10)
    for _ in range(4):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.randint(50, 80)
        # Cuerpo de tote
        draw.rectangle([x, y+s//4, x+s, y+s], outline=bag_color, width=2)
        # asas
        draw.arc([x+5, y, x+s//2, y+s//2], 180, 0, fill=bag_color, width=2)
        draw.arc([x+s//2, y, x+s-5, y+s//2], 180, 0, fill=bag_color, width=2)

    # Calendarios (rectangle with grid)
    cal_color = (255, 255, 255, 10)
    for _ in range(4):
        x = random.randint(0, w)
        y = random.randint(0, h)
        s = random.randint(50, 80)
        draw.rectangle([x, y, x+s, y+s*4//3], outline=cal_color, width=2)
        # grid interior
        for i in range(1, 5):
            draw.line([(x, y+i*s//4), (x+s, y+i*s//4)], fill=cal_color, width=1)

    # Suavizar el overlay
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=1.5))
    img.paste(overlay, (0, 0), overlay)

    # Glow corners
    accent = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ad = ImageDraw.Draw(accent)
    for r in range(450, 0, -8):
        alpha = int(40 * (1 - r/450))
        color = (*ORANGE, alpha) if r > 225 else (*PINK, alpha)
        ad.ellipse([w-r, -r//2, w+r, r], fill=color)
    accent = accent.filter(ImageFilter.GaussianBlur(radius=45))
    img.paste(accent, (0, 0), accent)

    accent2 = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ad2 = ImageDraw.Draw(accent2)
    for r in range(400, 0, -8):
        alpha = int(38 * (1 - r/400))
        color = (*PURPLE, alpha) if r > 200 else (*PINK, alpha)
        ad2.ellipse([-r, h-r, r, h+r//2], fill=color)
    accent2 = accent2.filter(ImageFilter.GaussianBlur(radius=45))
    img.paste(accent2, (0, 0), accent2)

    return img


# Funcion clave: alinear el logo COMO una letra K en el texto
def render_logo_text(img, draw, logo_h, font_text, text_rest, color_text, baseline_y, center_x):
    """Renderiza [LOGO]+texto centrado, con K alineada perfecto con texto.
    baseline_y: posicion Y donde el baseline del texto debe quedar
    center_x: posicion X del centro del bloque
    """
    logo = Image.open(LOGO_PATH)
    logo_w = int(logo.width * (logo_h / logo.height))

    # Calcular dimensiones del texto
    bbox = draw.textbbox((0, 0), text_rest, font=font_text)
    text_w = bbox[2] - bbox[0]
    # Altura desde top a baseline (cap height del font)
    ascent, descent = font_text.getmetrics()
    cap_h = ascent  # altura del top de capitales al baseline

    # Espaciado entre logo y texto (kerning)
    gap = 8

    total_w = logo_w + gap + text_w
    start_x = center_x - total_w // 2

    # Posicionar logo: top alineado para que la mayor parte quede al nivel cap-height
    # El logo es geometrico; visualmente alineamos su "top" con el cap-height del font
    # Aproximadamente, el "cap" del logo es el top, y su "descender" (la pierna) se extiende abajo
    # Para que se vea como una letra K, el TOP del logo = TOP de la O en texto
    # baseline_y - cap_h = posicion Y del top del texto
    text_top_y = baseline_y - cap_h
    # El logo top debe alinearse con el text top
    logo_y = text_top_y

    # Pegar logo
    logo_scaled = Image.open(LOGO_PATH).convert('RGBA').resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo_scaled, (start_x, logo_y), logo_scaled)

    # Renderizar texto a partir del fin del logo + gap
    text_x = start_x + logo_w + gap
    text_y = baseline_y - cap_h
    # Compensar baseline offset del PIL textbbox
    draw.text((text_x, text_y - bbox[1]), text_rest, fill=color_text, font=font_text)

    return total_w


# ==========================================
# TARJETA A - KODARASE PRINT (FRENTE)
# ==========================================

def make_print_front():
    img = make_product_bg(W, H)
    draw = ImageDraw.Draw(img)

    # Render "Kodarase" donde K es logo
    # Logo y texto deben tener misma altura visual
    f_brand = get_font(120, 'black')
    # Determinar altura del texto en pixels (cap height)
    ascent, descent = f_brand.getmetrics()
    cap_h = ascent

    # Logo del MISMO tamano que el cap height del font
    logo_h = cap_h

    center_x = W // 2
    # Baseline del texto
    baseline_y = 280

    render_logo_text(img, draw, logo_h, f_brand, 'odarase', WHITE, baseline_y, center_x)

    # ======= LINEA SEPARADORA =======
    line_y = baseline_y + 50
    line_w = 220
    draw.line([(W//2 - line_w//2, line_y), (W//2 + line_w//2, line_y)],
              fill=ORANGE, width=3)

    # ======= TAGLINE =======
    f_tag = get_font(32, 'bold')
    tag_main = 'PRINT  STUDIO'
    bbox = draw.textbbox((0, 0), tag_main, font=f_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 18), tag_main, fill=ORANGE, font=f_tag)

    # ======= SERVICIOS =======
    f_serv = get_font(22, 'regular')
    serv = "Lienzos · Pósteres · Marcos · Aluminio · Plexiglás · Tazas"
    bbox = draw.textbbox((0, 0), serv, font=f_serv)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 72), serv, fill=TEXT_2, font=f_serv)

    # ======= URL =======
    f_url = get_font(26, 'bold')
    url = 'kodarase.com'
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 75), url, fill=PINK, font=f_url)

    return img


def make_print_back():
    img = make_product_bg(W, H)
    draw = ImageDraw.Draw(img)

    # ======= HEADER: mini logo + Kodarase (K logo + odarase) =======
    f_smbrand = get_font(50, 'black')
    ascent, _ = f_smbrand.getmetrics()
    logo_h = ascent

    logo = Image.open(LOGO_PATH)
    logo_w = int(logo.width * (logo_h / logo.height))

    # Mini "Kodarase" header arriba a la izquierda
    header_x = MARGIN
    header_y_base = MARGIN + ascent  # baseline

    logo_scaled = Image.open(LOGO_PATH).convert('RGBA').resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo_scaled, (header_x, MARGIN), logo_scaled)

    text_x = header_x + logo_w + 6
    bbox = draw.textbbox((0, 0), 'odarase', font=f_smbrand)
    draw.text((text_x, MARGIN - bbox[1]), 'odarase', fill=WHITE, font=f_smbrand)

    # Print Studio debajo
    f_studio_sm = get_font(15, 'bold')
    draw.text((MARGIN + 8, MARGIN + logo_h + 8),
              'P R I N T   S T U D I O', fill=ORANGE, font=f_studio_sm)

    # ======= DATOS CLIENTE =======
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


# ==========================================
# TARJETA B - KODARASE DIGITAL (FRENTE)
# ==========================================

def make_universal_front():
    img = make_product_bg(W, H)
    draw = ImageDraw.Draw(img)

    # KODARASE en mayusculas grandes con K-logo
    f_brand = get_font(150, 'black')
    ascent, _ = f_brand.getmetrics()
    cap_h = ascent
    logo_h = cap_h

    center_x = W // 2
    baseline_y = 280

    render_logo_text(img, draw, logo_h, f_brand, 'ODARASE', WHITE, baseline_y, center_x)

    # Linea
    line_y = baseline_y + 50
    line_w = 220
    draw.line([(W//2 - line_w//2, line_y), (W//2 + line_w//2, line_y)],
              fill=ORANGE, width=3)

    # Tagline
    f_tag = get_font(32, 'bold')
    tag_main = 'DIGITAL  STUDIO'
    bbox = draw.textbbox((0, 0), tag_main, font=f_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 18), tag_main, fill=ORANGE, font=f_tag)

    # Servicios
    f_serv = get_font(22, 'regular')
    serv = "Web · Marketing · SEO · Automatización · Prints"
    bbox = draw.textbbox((0, 0), serv, font=f_serv)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 72), serv, fill=TEXT_2, font=f_serv)

    # URL
    f_url = get_font(26, 'bold')
    url = 'kodarase.com'
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 75), url, fill=PINK, font=f_url)

    return img


def make_universal_back():
    img = make_product_bg(W, H)
    draw = ImageDraw.Draw(img)

    # Header
    f_smbrand = get_font(50, 'black')
    ascent, _ = f_smbrand.getmetrics()
    logo_h = ascent

    logo = Image.open(LOGO_PATH)
    logo_w = int(logo.width * (logo_h / logo.height))

    logo_scaled = Image.open(LOGO_PATH).convert('RGBA').resize((logo_w, logo_h), Image.LANCZOS)
    img.paste(logo_scaled, (MARGIN, MARGIN), logo_scaled)

    text_x = MARGIN + logo_w + 6
    bbox = draw.textbbox((0, 0), 'odarase', font=f_smbrand)
    draw.text((text_x, MARGIN - bbox[1]), 'odarase', fill=WHITE, font=f_smbrand)

    f_studio_sm = get_font(15, 'bold')
    draw.text((MARGIN + 8, MARGIN + logo_h + 8),
              'D I G I T A L   S T U D I O', fill=ORANGE, font=f_studio_sm)

    # Datos
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


print("Generando tarjetas v4...")
print_front = make_print_front()
print_front.save(os.path.join(OUT_DIR, 'tarjeta-print-front-v4.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-print-front-v4.png")

print_back = make_print_back()
print_back.save(os.path.join(OUT_DIR, 'tarjeta-print-back-v4.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-print-back-v4.png")

universal_front = make_universal_front()
universal_front.save(os.path.join(OUT_DIR, 'tarjeta-universal-front-v4.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-universal-front-v4.png")

universal_back = make_universal_back()
universal_back.save(os.path.join(OUT_DIR, 'tarjeta-universal-back-v4.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-universal-back-v4.png")
print("\nDONE")
