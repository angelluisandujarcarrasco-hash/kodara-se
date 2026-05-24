"""
Enhance v8: mejora calidad SIN cambiar composicion.
- Sharpening global suave
- Sharpening fuerte en los ojos del papa
- Upscale a 4K con Lanczos
"""
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT = "regalo-papa-v8.png"
OUTPUT = "regalo-papa-v9-enhanced.png"

# Coords del papa en v8 (detectadas previamente)
PAPA_FACE = {"x": 1210, "y": 286, "w": 234, "h": 234}

print(f"Cargando {INPUT}...")
img = cv2.imread(INPUT)
H, W = img.shape[:2]
print(f"Tamano original: {W}x{H}")

# ==== 1. Detectar ojos en la cara del papa ====
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Recortar cara del papa (con margen)
fx, fy, fw, fh = PAPA_FACE["x"], PAPA_FACE["y"], PAPA_FACE["w"], PAPA_FACE["h"]
margin = 20
crop_x1 = max(0, fx - margin)
crop_y1 = max(0, fy - margin)
crop_x2 = min(W, fx + fw + margin)
crop_y2 = min(H, fy + fh + margin)
face_crop = img[crop_y1:crop_y2, crop_x1:crop_x2]
gray_face = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)

# Detectar ojos en la cara
eyes = eye_cascade.detectMultiScale(gray_face, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20))
print(f"\nOjos detectados en cara del papa: {len(eyes)}")

# Convertir coords de eyes a coords globales (de la imagen completa)
eye_regions = []
for (ex, ey, ew, eh) in eyes:
    gx = crop_x1 + ex
    gy = crop_y1 + ey
    print(f"  Ojo: x={gx}, y={gy}, w={ew}, h={eh}")
    eye_regions.append((gx, gy, ew, eh))

# ==== 2. Aplicar sharpening fuerte en los ojos del papa ====
def sharpen_region(image, x, y, w, h, strength=2.0):
    """Aplica unsharp mask fuerte en una region."""
    region = image[y:y+h, x:x+w].copy()
    # Crear blur
    blurred = cv2.GaussianBlur(region, (0, 0), sigmaX=1.5)
    # Unsharp mask: original + (original - blur) * strength
    sharpened = cv2.addWeighted(region, 1.0 + strength, blurred, -strength, 0)
    image[y:y+h, x:x+w] = sharpened
    return image

# Aplicar sharpening fuerte en cada ojo detectado
for (ex, ey, ew, eh) in eye_regions:
    # Expandir region para incluir cejas y zona alrededor del ojo
    pad_x = int(ew * 0.3)
    pad_y = int(eh * 0.3)
    px = max(0, ex - pad_x)
    py = max(0, ey - pad_y)
    pw = min(W - px, ew + 2 * pad_x)
    ph = min(H - py, eh + 2 * pad_y)
    img = sharpen_region(img, px, py, pw, ph, strength=1.8)
    print(f"  Sharpened eye region @ ({px},{py}) {pw}x{ph}")

# ==== 3. Sharpening global suave (todo el cuadro) ====
print("\nAplicando sharpening global suave...")
blurred_global = cv2.GaussianBlur(img, (0, 0), sigmaX=1.2)
img = cv2.addWeighted(img, 1.4, blurred_global, -0.4, 0)

# ==== 4. Upscale a 4K con Lanczos ====
TARGET_W = 5120  # ~4K equivalente
scale = TARGET_W / W
new_w = TARGET_W
new_h = int(H * scale)
print(f"\nUpscaling a {new_w}x{new_h} (Lanczos)...")
img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

# ==== 5. Saturacion/contraste sutil para vivacidad ====
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Pequeno boost de contraste
enhancer = ImageEnhance.Contrast(img_pil)
img_pil = enhancer.enhance(1.05)

# Pequeno boost de saturacion (luz dorada se ve mas calida)
enhancer = ImageEnhance.Color(img_pil)
img_pil = enhancer.enhance(1.08)

# Pequeno boost de brillo
enhancer = ImageEnhance.Brightness(img_pil)
img_pil = enhancer.enhance(1.02)

# Sharpness adicional via PIL (mas suave que cv2)
img_pil = img_pil.filter(ImageFilter.UnsharpMask(radius=1.5, percent=120, threshold=3))

print(f"\nGuardando {OUTPUT}...")
img_pil.save(OUTPUT, "PNG", optimize=True)
print(f"OK - Tamano final: {img_pil.size}")
