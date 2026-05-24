"""
Enhance v8 v2: sharpening manual en ojos del papa.
"""
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT = "regalo-papa-v8.png"
OUTPUT = "regalo-papa-v10-enhanced.png"

PAPA_FACE = {"x": 1210, "y": 286, "w": 234, "h": 234}

print(f"Cargando {INPUT}...")
img = cv2.imread(INPUT)
H, W = img.shape[:2]
print(f"Tamano original: {W}x{H}")

# ==== Posiciones manuales de los ojos del papa ====
fx, fy, fw, fh = PAPA_FACE["x"], PAPA_FACE["y"], PAPA_FACE["w"], PAPA_FACE["h"]
# Eyes son aprox 35-45% Y, 25-75% X (con espacio entre ellos)
eye_y_top = fy + int(fh * 0.30)
eye_y_bot = fy + int(fh * 0.50)
left_eye_x1 = fx + int(fw * 0.18)
left_eye_x2 = fx + int(fw * 0.45)
right_eye_x1 = fx + int(fw * 0.55)
right_eye_x2 = fx + int(fw * 0.82)

print(f"\nOjo izq: ({left_eye_x1},{eye_y_top}) - ({left_eye_x2},{eye_y_bot})")
print(f"Ojo der: ({right_eye_x1},{eye_y_top}) - ({right_eye_x2},{eye_y_bot})")

# Tambien la zona completa de los ojos (incluyendo cejas)
brow_to_eye_y1 = fy + int(fh * 0.22)
brow_to_eye_y2 = fy + int(fh * 0.55)
brow_to_eye_x1 = fx + int(fw * 0.12)
brow_to_eye_x2 = fx + int(fw * 0.88)

def sharpen_region(image, x1, y1, x2, y2, strength=2.5, sigma=1.0):
    """Aplica unsharp mask muy fuerte en una region."""
    region = image[y1:y2, x1:x2].copy()
    blurred = cv2.GaussianBlur(region, (0, 0), sigmaX=sigma)
    sharpened = cv2.addWeighted(region, 1.0 + strength, blurred, -strength, 0)
    # Anadir saturacion local sutil
    image[y1:y2, x1:x2] = sharpened
    return image

# 1. Sharpening MUY fuerte en zona ojos+cejas
print("\nSharpening fuerte en ojos+cejas del papa...")
img = sharpen_region(img, brow_to_eye_x1, brow_to_eye_y1, brow_to_eye_x2, brow_to_eye_y2, strength=2.2, sigma=0.8)

# 2. Sharpening EXTRA fuerte en cada ojo individualmente
img = sharpen_region(img, left_eye_x1, eye_y_top, left_eye_x2, eye_y_bot, strength=1.5, sigma=0.6)
img = sharpen_region(img, right_eye_x1, eye_y_top, right_eye_x2, eye_y_bot, strength=1.5, sigma=0.6)

# 3. Tambien sharpening en caras de abuelo y abuela (no tan fuerte)
ABUELO_FACE = {"x": 779, "y": 410, "w": 181, "h": 181}
ABUELA_FACE = {"x": 1601, "y": 591, "w": 280, "h": 280}

for face in [ABUELO_FACE, ABUELA_FACE]:
    x1 = face["x"]
    y1 = face["y"]
    x2 = x1 + face["w"]
    y2 = y1 + face["h"]
    img = sharpen_region(img, x1, y1, x2, y2, strength=1.2, sigma=1.0)

# 4. Sharpening global suave (todo el cuadro)
print("Sharpening global suave...")
blurred_global = cv2.GaussianBlur(img, (0, 0), sigmaX=1.2)
img = cv2.addWeighted(img, 1.5, blurred_global, -0.5, 0)

# 5. Upscale a 4K con Lanczos
TARGET_W = 5120
scale = TARGET_W / W
new_w = TARGET_W
new_h = int(H * scale)
print(f"Upscaling a {new_w}x{new_h}...")
img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

# 6. Post-process PIL
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Boost contraste y saturacion
img_pil = ImageEnhance.Contrast(img_pil).enhance(1.06)
img_pil = ImageEnhance.Color(img_pil).enhance(1.10)
img_pil = ImageEnhance.Brightness(img_pil).enhance(1.02)
img_pil = ImageEnhance.Sharpness(img_pil).enhance(1.3)

# Unsharp mask final via PIL
img_pil = img_pil.filter(ImageFilter.UnsharpMask(radius=1.8, percent=140, threshold=2))

print(f"\nGuardando {OUTPUT}...")
img_pil.save(OUTPUT, "PNG", optimize=True)
print(f"OK - Tamano final: {img_pil.size}")
