"""
Tarjetas v5 - K BIEN ALINEADA + BG con productos REALES.
- Calcular bbox real del K-logo (sin transparente)
- Alinear con TOP del texto
- BG con collage de productos reales (lienzos, posters, etc.)
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import random

OUT_DIR = r"C:\Users\lucie\kodara-se\tarjetas"
PROD_DIR = os.path.join(OUT_DIR, 'productos')
LOGO_PATH = os.path.join(OUT_DIR, 'logo-kodara-transparent.png')

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


def get_logo_visible_bbox():
    """Devuelve la bbox de los pixeles VISIBLES (no transparentes) del logo."""
    logo = Image.open(LOGO_PATH).convert('RGBA')
    bbox = logo.getbbox()  # bbox de pixeles no transparentes
    return logo, bbox


def make_product_collage_bg(w, h, theme='print'):
    """Background con collage de productos reales, blurred y oscurecidos."""
    img = Image.new('RGB', (w, h), BG)
    px = img.load()
    for y in range(h):
        t = y / h
        r = int(BG[0] + (BG_DEEP[0] - BG[0]) * t)
        g = int(BG[1] + (BG_DEEP[1] - BG[1]) * t)
        b = int(BG[2] + (BG_DEEP[2] - BG[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)

    # Cargar productos
    if theme == 'print':
        prods = ['lienzo.png', 'poster.png', 'marco-metal.png',
                 'aluminio.png', 'plexiglas.png', 'espuma.png',
                 'madera.png', 'colgador.png']
    else:
        # Para digital, usar mas variedad
        prods = ['lienzo.png', 'poster.png', 'marco-metal.png',
                 'aluminio.png', 'plexiglas.png', 'espuma.png']

    random.seed(11)

    # Tile pattern: 4 cols x 3 rows = 12 imagenes
    tile_w = w // 4
    tile_h = h // 3
    positions = []
    for col in range(4):
        for row in range(3):
            positions.append((col * tile_w, row * tile_h))

    # Shuffle pero deterministico
    random.shuffle(positions)

    collage = Image.new('RGB', (w, h), BG)
    for i, pos in enumerate(positions):
        prod_file = prods[i % len(prods)]
        prod_path = os.path.join(PROD_DIR, prod_file)
        if not os.path.exists(prod_path):
            continue
        try:
            p = Image.open(prod_path).convert('RGB')
            # Resize a tile
            p_resized = p.resize((tile_w, tile_h), Image.LANCZOS)
            collage.paste(p_resized, pos)
        except Exception as e:
            print(f"WARN {prod_file}: {e}")

    # Blur el collage para que sea fondo no protagonista
    collage_blurred = collage.filter(ImageFilter.GaussianBlur(radius=18))

    # Reducir brillo
    enhancer = ImageEnhance.Brightness(collage_blurred)
    collage_dark = enhancer.enhance(0.35)  # 35% del brillo original

    # Mezclar con el bg base (50/50)
    overlay = Image.blend(img, collage_dark, 0.55)

    # Overlay dark gradient encima para legibilidad de texto en centro
    dark_overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    dod = ImageDraw.Draw(dark_overlay)
    # Vignette: oscurecer centro un poco menos, bordes mas
    # Pero queremos texto LEGIBLE en centro, asi que oscurecemos centro
    for r in range(min(w, h) // 2, 0, -10):
        alpha = int(60 * (r / (min(w, h) // 2)))
        # Solo dibujar gradiente sutil
    # Mejor: capa semitransparente uniforme oscura
    dark_layer = Image.new('RGBA', (w, h), (0, 0, 0, 80))
    overlay_rgba = overlay.convert('RGBA')
    final = Image.alpha_composite(overlay_rgba, dark_layer)

    # Glow accents en esquinas
    accent = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ad = ImageDraw.Draw(accent)
    for r in range(380, 0, -8):
        alpha = int(30 * (1 - r/380))
        color = (*ORANGE, alpha) if r > 190 else (*PINK, alpha)
        ad.ellipse([w-r, -r//2, w+r, r], fill=color)
    accent = accent.filter(ImageFilter.GaussianBlur(radius=35))
    final = Image.alpha_composite(final, accent)

    accent2 = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ad2 = ImageDraw.Draw(accent2)
    for r in range(380, 0, -8):
        alpha = int(30 * (1 - r/380))
        color = (*PURPLE, alpha) if r > 190 else (*PINK, alpha)
        ad2.ellipse([-r, h-r, r, h+r//2], fill=color)
    accent2 = accent2.filter(ImageFilter.GaussianBlur(radius=35))
    final = Image.alpha_composite(final, accent2)

    return final.convert('RGB')


def render_logo_text_aligned(img, draw, font_text, text_rest, color_text, baseline_y, center_x, logo_scale=1.0):
    """Renderiza [LOGO]+texto centrado. La K se alinea con cap-height del texto.
    Usa la bbox real del logo (no del archivo)."""
    # Cap height del font
    ascent, descent = font_text.getmetrics()
    cap_h = int(ascent * 0.78)  # cap height es ~78% del ascent en fonts modernos

    # Cargar logo y obtener bbox visible
    logo_orig = Image.open(LOGO_PATH).convert('RGBA')
    visible_bbox = logo_orig.getbbox()  # left, top, right, bottom
    # Crop al bbox visible
    logo_visible = logo_orig.crop(visible_bbox)
    vis_w = logo_visible.width
    vis_h = logo_visible.height

    # Scale: queremos que el ancho visible del K sea proporcional a la altura del texto
    # Hacemos que la altura visible del K sea igual al cap_h del texto
    target_logo_h = int(cap_h * logo_scale)
    ratio = target_logo_h / vis_h
    target_logo_w = int(vis_w * ratio)

    logo_scaled = logo_visible.resize((target_logo_w, target_logo_h), Image.LANCZOS)

    # Dimensiones del texto
    bbox = draw.textbbox((0, 0), text_rest, font=font_text)
    text_w = bbox[2] - bbox[0]
    text_offset_top = bbox[1]  # offset desde top del bbox a top real
    text_top_y = baseline_y - cap_h

    # Espaciado entre logo y texto
    gap = 14

    total_w = target_logo_w + gap + text_w
    start_x = center_x - total_w // 2

    # Pegar logo: top alineado con top del texto
    logo_y = text_top_y
    img.paste(logo_scaled, (start_x, logo_y), logo_scaled)

    # Renderizar texto
    text_x = start_x + target_logo_w + gap
    text_y = text_top_y - text_offset_top
    draw.text((text_x, text_y), text_rest, fill=color_text, font=font_text)

    return total_w


# ==========================================
# TARJETA A - PRINT
# ==========================================

def make_print_front():
    img = make_product_collage_bg(W, H, theme='print')
    draw = ImageDraw.Draw(img)

    f_brand = get_font(120, 'black')
    baseline_y = 290
    center_x = W // 2

    render_logo_text_aligned(img, draw, f_brand, 'odarase', WHITE, baseline_y, center_x, logo_scale=1.05)

    # Linea
    line_y = baseline_y + 55
    draw.line([(W//2 - 110, line_y), (W//2 + 110, line_y)], fill=ORANGE, width=3)

    # Tagline
    f_tag = get_font(32, 'bold')
    tag_main = 'PRINT  STUDIO'
    bbox = draw.textbbox((0, 0), tag_main, font=f_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 18), tag_main, fill=ORANGE, font=f_tag)

    # Servicios
    f_serv = get_font(22, 'regular')
    serv = "Lienzos · Pósteres · Marcos · Aluminio · Plexiglás · Tazas"
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


def make_print_back():
    img = make_product_collage_bg(W, H, theme='print')
    draw = ImageDraw.Draw(img)

    # Header mini Kodarase
    f_smbrand = get_font(50, 'black')
    ascent, _ = f_smbrand.getmetrics()
    cap_h = int(ascent * 0.78)

    logo_orig = Image.open(LOGO_PATH).convert('RGBA')
    visible_bbox = logo_orig.getbbox()
    logo_visible = logo_orig.crop(visible_bbox)
    target_h = cap_h
    ratio = target_h / logo_visible.height
    target_w = int(logo_visible.width * ratio)
    logo_scaled = logo_visible.resize((target_w, target_h), Image.LANCZOS)

    text_top = MARGIN
    img.paste(logo_scaled, (MARGIN, text_top), logo_scaled)

    text_x = MARGIN + target_w + 8
    bbox = draw.textbbox((0, 0), 'odarase', font=f_smbrand)
    draw.text((text_x, text_top - bbox[1]), 'odarase', fill=WHITE, font=f_smbrand)

    f_studio_sm = get_font(15, 'bold')
    draw.text((MARGIN + 8, text_top + target_h + 8),
              'P R I N T   S T U D I O', fill=ORANGE, font=f_studio_sm)

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

    draw.line([(W//2 - 80, cy + 5), (W//2 + 80, cy + 5)], fill=PINK, width=2)

    f_contact = get_font(24, 'regular')
    email = 'kodarase@gmail.com'
    bbox = draw.textbbox((0, 0), email, font=f_contact)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 32), email, fill=TEXT_2, font=f_contact)

    f_url = get_font(26, 'bold')
    url = 'kodarase.com'
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 75), url, fill=PINK, font=f_url)

    return img


# ==========================================
# TARJETA B - UNIVERSAL
# ==========================================

def make_universal_front():
    img = make_product_collage_bg(W, H, theme='digital')
    draw = ImageDraw.Draw(img)

    f_brand = get_font(150, 'black')
    baseline_y = 290
    render_logo_text_aligned(img, draw, f_brand, 'ODARASE', WHITE, baseline_y, W // 2, logo_scale=1.05)

    line_y = baseline_y + 55
    draw.line([(W//2 - 110, line_y), (W//2 + 110, line_y)], fill=ORANGE, width=3)

    f_tag = get_font(32, 'bold')
    tag_main = 'DIGITAL  STUDIO'
    bbox = draw.textbbox((0, 0), tag_main, font=f_tag)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 18), tag_main, fill=ORANGE, font=f_tag)

    f_serv = get_font(22, 'regular')
    serv = "Web · Marketing · SEO · Automatización · Prints"
    bbox = draw.textbbox((0, 0), serv, font=f_serv)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, line_y + 72), serv, fill=TEXT_2, font=f_serv)

    f_url = get_font(26, 'bold')
    url = 'kodarase.com'
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, H - 75), url, fill=PINK, font=f_url)

    return img


def make_universal_back():
    img = make_product_collage_bg(W, H, theme='digital')
    draw = ImageDraw.Draw(img)

    f_smbrand = get_font(50, 'black')
    ascent, _ = f_smbrand.getmetrics()
    cap_h = int(ascent * 0.78)

    logo_orig = Image.open(LOGO_PATH).convert('RGBA')
    visible_bbox = logo_orig.getbbox()
    logo_visible = logo_orig.crop(visible_bbox)
    ratio = cap_h / logo_visible.height
    target_w = int(logo_visible.width * ratio)
    logo_scaled = logo_visible.resize((target_w, cap_h), Image.LANCZOS)

    img.paste(logo_scaled, (MARGIN, MARGIN), logo_scaled)

    text_x = MARGIN + target_w + 8
    bbox = draw.textbbox((0, 0), 'odarase', font=f_smbrand)
    draw.text((text_x, MARGIN - bbox[1]), 'odarase', fill=WHITE, font=f_smbrand)

    f_studio_sm = get_font(15, 'bold')
    draw.text((MARGIN + 8, MARGIN + cap_h + 8),
              'D I G I T A L   S T U D I O', fill=ORANGE, font=f_studio_sm)

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

    draw.line([(W//2 - 80, cy + 5), (W//2 + 80, cy + 5)], fill=PINK, width=2)

    f_contact = get_font(24, 'regular')
    email = 'kodarase@gmail.com'
    bbox = draw.textbbox((0, 0), email, font=f_contact)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 32), email, fill=TEXT_2, font=f_contact)

    f_url = get_font(26, 'bold')
    url = 'kodarase.com'
    bbox = draw.textbbox((0, 0), url, font=f_url)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, cy + 75), url, fill=PINK, font=f_url)

    return img


print("Generando tarjetas v5...")
print_front = make_print_front()
print_front.save(os.path.join(OUT_DIR, 'tarjeta-print-front-v5.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-print-front-v5.png")

print_back = make_print_back()
print_back.save(os.path.join(OUT_DIR, 'tarjeta-print-back-v5.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-print-back-v5.png")

universal_front = make_universal_front()
universal_front.save(os.path.join(OUT_DIR, 'tarjeta-universal-front-v5.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-universal-front-v5.png")

universal_back = make_universal_back()
universal_back.save(os.path.join(OUT_DIR, 'tarjeta-universal-back-v5.png'), 'PNG', dpi=(300, 300))
print("OK tarjeta-universal-back-v5.png")
