"""
Face-swap: pegar la cara real de mama (#27) sobre v4 (winner version).
Usa seamlessClone para Poisson blending profesional.
"""
import cv2
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = "familia2-v4-seedream.png"
FACE_SRC = "mama-cara-real.png"
OUT = "familia2-v12-faceswap.png"

print(f"Cargando base {BASE}...")
base = cv2.imread(BASE)
H, W = base.shape[:2]
print(f"Base tamano: {W}x{H}")

print(f"Cargando cara fuente {FACE_SRC}...")
src_img = cv2.imread(FACE_SRC)
sH, sW = src_img.shape[:2]
print(f"Fuente tamano: {sW}x{sH}")

# Detectar cara en source
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
src_gray = cv2.cvtColor(src_img, cv2.COLOR_BGR2GRAY)
src_faces = face_cascade.detectMultiScale(src_gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
print(f"\nCaras en fuente: {len(src_faces)}")

if len(src_faces) == 0:
    print("FAIL: no se detecto cara en fuente")
    sys.exit(1)

# Usar la cara mas grande
src_faces_sorted = sorted(src_faces, key=lambda f: f[2]*f[3], reverse=True)
sx, sy, sw, sh = src_faces_sorted[0]
print(f"Cara fuente: ({sx},{sy}) {sw}x{sh}")

# Detectar caras en base
base_gray = cv2.cvtColor(base, cv2.COLOR_BGR2GRAY)
base_faces = face_cascade.detectMultiScale(base_gray, scaleFactor=1.05, minNeighbors=4, minSize=(100, 100))
print(f"\nCaras en base: {len(base_faces)}")

# Filtrar y ordenar por X (las 3 personas estan dispuestas izq->der)
base_faces_filtered = [f for f in base_faces if f[2] >= 150 and f[3] >= 150]
base_faces_sorted_x = sorted(base_faces_filtered, key=lambda f: f[0])  # por X
print(f"Caras grandes en base (ordenadas izq->der):")
for f in base_faces_sorted_x:
    print(f"  ({f[0]},{f[1]}) {f[2]}x{f[3]}")

# La mama esta en el CENTRO (segunda por X)
if len(base_faces_sorted_x) < 3:
    print("FAIL: no se detectaron 3 caras")
    sys.exit(1)

mama_face = base_faces_sorted_x[1]
bx, by, bw, bh = mama_face
print(f"\nCara mama en base (centro): ({bx},{by}) {bw}x{bh}")

def expand_box(box, img_shape, expand_w=0.3, expand_top=0.5, expand_bottom=0.3):
    x, y, w, h = box
    H, W = img_shape[:2]
    ex_w = int(w * expand_w)
    x1 = max(0, x - ex_w)
    y1 = max(0, y - int(h * expand_top))
    x2 = min(W, x + w + ex_w)
    y2 = min(H, y + h + int(h * expand_bottom))
    return (x1, y1, x2 - x1, y2 - y1)

def color_transfer_lab(source_bgr, target_bgr):
    """LAB color transfer para matching skin tone."""
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

# Expandir crop de fuente (toda la cara visible)
src_exp = expand_box((sx, sy, sw, sh), src_img.shape, expand_w=0.2, expand_top=0.4, expand_bottom=0.25)
sxe, sye, swe, she = src_exp
src_face_crop = src_img[sye:sye+she, sxe:sxe+swe].copy()
print(f"\nFuente crop expandido: {swe}x{she}")

# Expandir crop de destino (mismo ratio)
tgt_exp = expand_box((bx, by, bw, bh), base.shape, expand_w=0.2, expand_top=0.4, expand_bottom=0.25)
tx, ty, tw, th = tgt_exp
print(f"Destino crop: {tw}x{th} @ ({tx},{ty})")

# Resize source para que case con destino
src_resized = cv2.resize(src_face_crop, (tw, th), interpolation=cv2.INTER_LANCZOS4)

# Color matching (LAB)
dst_area = base[ty:ty+th, tx:tx+tw].copy()
src_color_matched = color_transfer_lab(src_resized, dst_area)

# Crear mascara eliptica
mask = np.zeros((th, tw), dtype=np.uint8)
cv2.ellipse(mask,
            center=(tw // 2, th // 2),
            axes=(int(tw * 0.42), int(th * 0.46)),
            angle=0, startAngle=0, endAngle=360,
            color=255, thickness=-1)

# seamlessClone
center = (tx + tw // 2, ty + th // 2)
result = cv2.seamlessClone(src_color_matched, base, mask, center, cv2.NORMAL_CLONE)

print(f"\nSwap completado @ centro {center}")
cv2.imwrite(OUT, result)
print(f"Guardado: {OUT}")

# Tambien JPG para upload
from PIL import Image
im_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
im_pil.save(OUT.replace('.png', '.jpg'), 'JPEG', dpi=(300,300), quality=92, optimize=True)
print(f"Guardado JPG: {OUT.replace('.png', '.jpg')}")
