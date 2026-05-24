"""
Face-swap v2: usa cv2.seamlessClone para Poisson blending profesional.
Las caras se funden invisiblemente con el fondo.
"""
import cv2
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "regalo-papa-v4-seedream.png"

TARGETS = {
    "abuelo": {"x": 779, "y": 410, "w": 181, "h": 181},
    "papa":   {"x": 1210, "y": 286, "w": 234, "h": 234},
    "abuela": {"x": 1601, "y": 591, "w": 280, "h": 280},
}

SOURCES = {
    "papa":   {"file": "ref-13.jpg",          "face": (213, 381, 216, 216)},
    "abuelo": {"file": "src-abuelo-cap.jpg",  "face": (12,  55,  147, 147)},
    "abuela": {"file": "src-abuela-pink.jpg", "face": (254, 368, 238, 238)},
}

def expand_box(face_box, img_shape, expand=0.7, up_extra=0.7, down_extra=0.5):
    """Expande el bounding box, mas hacia arriba (pelo) y un poco abajo (barbilla)."""
    x, y, w, h = face_box
    H, W = img_shape[:2]
    ex_w = int(w * expand)
    ex_h = int(h * expand)
    x1 = max(0, x - ex_w // 2)
    y1 = max(0, y - int(ex_h * up_extra))
    x2 = min(W, x + w + ex_w // 2)
    y2 = min(H, y + h + int(ex_h * down_extra))
    return (x1, y1, x2 - x1, y2 - y1)

def color_transfer_lab(source_bgr, target_bgr):
    """Transfiere paleta de color de target a source usando LAB color space."""
    src_lab = cv2.cvtColor(source_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)
    tgt_lab = cv2.cvtColor(target_bgr, cv2.COLOR_BGR2LAB).astype(np.float32)

    for ch in range(3):
        src_ch = src_lab[:, :, ch]
        tgt_ch = tgt_lab[:, :, ch]
        src_mean, src_std = src_ch.mean(), src_ch.std()
        tgt_mean, tgt_std = tgt_ch.mean(), tgt_ch.std()
        if src_std > 1:
            src_lab[:, :, ch] = ((src_ch - src_mean) * (tgt_std / src_std)) + tgt_mean

    src_lab = np.clip(src_lab, 0, 255).astype(np.uint8)
    return cv2.cvtColor(src_lab, cv2.COLOR_LAB2BGR)

def swap_face_seamless(base_bgr, person_key):
    src_info = SOURCES[person_key]
    tgt = TARGETS[person_key]

    # 1. Cargar fuente
    src_full = cv2.imread(src_info["file"])

    # 2. Expandir crop de la cara fuente
    src_box = expand_box(src_info["face"], src_full.shape, expand=0.5, up_extra=0.5, down_extra=0.3)
    sx, sy, sw, sh = src_box
    src_face = src_full[sy:sy+sh, sx:sx+sw].copy()

    # 3. Calcular bounding box destino
    tgt_face_box = (tgt["x"], tgt["y"], tgt["w"], tgt["h"])
    tgt_box = expand_box(tgt_face_box, base_bgr.shape, expand=0.5, up_extra=0.5, down_extra=0.3)
    tx, ty, tw, th = tgt_box

    # 4. Resize source para que coincida con destino
    src_resized = cv2.resize(src_face, (tw, th), interpolation=cv2.INTER_LANCZOS4)

    # 5. Color matching usando LAB color space (paleta de luz dorada)
    dst_area = base_bgr[ty:ty+th, tx:tx+tw].copy()
    src_color_matched = color_transfer_lab(src_resized, dst_area)

    # 6. Crear mascara eliptica para seamlessClone
    mask = np.zeros((th, tw), dtype=np.uint8)
    cv2.ellipse(mask,
                center=(tw // 2, th // 2),
                axes=(int(tw * 0.40), int(th * 0.45)),
                angle=0, startAngle=0, endAngle=360,
                color=255, thickness=-1)

    # 7. seamlessClone: Poisson blending - bordes invisibles
    center = (tx + tw // 2, ty + th // 2)
    result = cv2.seamlessClone(src_color_matched, base_bgr, mask, center, cv2.NORMAL_CLONE)

    print(f"  OK {person_key}: cara {sw}x{sh} -> destino {tw}x{th} @ centro {center}")
    return result

# === MAIN ===
print(f"Abriendo base: {BASE}")
base = cv2.imread(BASE)
print(f"Tamano: {base.shape[1]}x{base.shape[0]}")

print("\nHaciendo face-swap con seamlessClone...")
base = swap_face_seamless(base, "papa")
base = swap_face_seamless(base, "abuelo")
base = swap_face_seamless(base, "abuela")

OUT = "regalo-papa-v6-seamless.png"
cv2.imwrite(OUT, base)
print(f"\nGuardado: {OUT}")
