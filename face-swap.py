"""
Face-swap: pega las caras reales sobre la version AI v4-seedream.
"""
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "regalo-papa-v4-seedream.png"

# Coordenadas de caras en el BASE (detectadas por OpenCV)
TARGETS = {
    "abuelo": {"x": 779, "y": 410, "w": 181, "h": 181},
    "papa":   {"x": 1210, "y": 286, "w": 234, "h": 234},
    "abuela": {"x": 1601, "y": 591, "w": 280, "h": 280},
}

# Fuentes y sus caras detectadas
SOURCES = {
    "papa":   {"file": "ref-13.jpg",         "face": (213, 381, 216, 216)},
    "abuelo": {"file": "src-abuelo-cap.jpg", "face": (12,  55,  147, 147)},
    "abuela": {"file": "src-abuela-pink.jpg","face": (254, 368, 238, 238)},
}

def expand_face_crop(face_box, img_shape, expand=0.55):
    """Expande el bounding box de la cara para incluir frente, pelo y barbilla."""
    x, y, w, h = face_box
    H, W = img_shape[:2]
    ex_w = int(w * expand)
    ex_h = int(h * expand)
    # Mas expansion hacia arriba (pelo) y abajo (cuello)
    x1 = max(0, x - ex_w // 2)
    y1 = max(0, y - int(ex_h * 0.7))  # mas arriba (pelo)
    x2 = min(W, x + w + ex_w // 2)
    y2 = min(H, y + h + int(ex_h * 0.5))  # un poco abajo (barbilla)
    return (x1, y1, x2 - x1, y2 - y1)

def color_match(src_pil, dst_pil):
    """Ajusta brillo/saturacion de src_pil para que case con dst_pil."""
    src_arr = np.array(src_pil.convert("RGB"))
    dst_arr = np.array(dst_pil.convert("RGB"))
    src_mean = src_arr.reshape(-1, 3).mean(axis=0)
    dst_mean = dst_arr.reshape(-1, 3).mean(axis=0)
    # Shift por canal
    diff = dst_mean - src_mean
    adjusted = src_arr.astype(np.float32) + diff
    adjusted = np.clip(adjusted, 0, 255).astype(np.uint8)
    return Image.fromarray(adjusted)

def make_oval_mask(size, feather=40):
    """Crea una mascara eliptica con bordes suaves (feathered)."""
    w, h = size
    mask = Image.new("L", size, 0)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    # Elipse interna (mas pequena para que el feather no se salga)
    margin_x = int(w * 0.05)
    margin_y = int(h * 0.05)
    draw.ellipse([margin_x, margin_y, w - margin_x, h - margin_y], fill=255)
    # Aplicar Gaussian blur para feather edges
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    return mask

def swap_face(base_pil, person_key):
    """Swap face for one person."""
    src_info = SOURCES[person_key]
    tgt = TARGETS[person_key]

    # 1. Abrir foto fuente
    src_img = cv2.imread(src_info["file"])
    src_pil_full = Image.open(src_info["file"]).convert("RGB")

    # 2. Expandir el crop de la cara fuente
    src_face_box = src_info["face"]
    exp_box = expand_face_crop(src_face_box, src_img.shape, expand=0.7)
    sx, sy, sw, sh = exp_box
    src_face = src_pil_full.crop((sx, sy, sx + sw, sy + sh))

    # 3. Calcular tamano del swap en el base, expandiendo similarmente
    tgt_face_box = (tgt["x"], tgt["y"], tgt["w"], tgt["h"])
    base_arr = np.array(base_pil)
    tgt_exp = expand_face_crop(tgt_face_box, base_arr.shape, expand=0.7)
    tx, ty, tw, th = tgt_exp

    # 4. Resize source crop al tamano destino
    src_resized = src_face.resize((tw, th), Image.LANCZOS)

    # 5. Color matching: usar la zona destino como referencia
    dst_crop = base_pil.crop((tx, ty, tx + tw, ty + th))
    src_color_matched = color_match(src_resized, dst_crop)

    # 6. Suavizar un poco la imagen fuente para que case con el render AI
    src_smooth = src_color_matched.filter(ImageFilter.GaussianBlur(0.6))

    # 7. Crear mascara eliptica con feather
    mask = make_oval_mask((tw, th), feather=int(min(tw, th) * 0.10))

    # 8. Pegar
    base_pil.paste(src_smooth, (tx, ty), mask)

    print(f"  OK swap {person_key}: src crop {sw}x{sh} -> dst {tw}x{th} @ ({tx},{ty})")
    return base_pil

# === MAIN ===
print(f"Abriendo base: {BASE}")
base_pil = Image.open(BASE).convert("RGB")
print(f"Tamano: {base_pil.size}")

print("\nHaciendo face-swap...")
base_pil = swap_face(base_pil, "papa")
base_pil = swap_face(base_pil, "abuelo")
base_pil = swap_face(base_pil, "abuela")

OUT = "regalo-papa-v5-hibrido.png"
base_pil.save(OUT, "PNG", optimize=True)
print(f"\nGuardado: {OUT}")
print(f"Tamano final: {base_pil.size}")
