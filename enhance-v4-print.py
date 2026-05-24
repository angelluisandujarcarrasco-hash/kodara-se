"""
v4 print-ready para 45x60 cm: upscale 4x + sharpening en ojos + DPI 300.
"""
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT = "familia2-v4-seedream.png"
OUT_PNG = "familia2-v14-print.png"
OUT_JPG = "familia2-v14-print.jpg"

print(f"Cargando {INPUT}...")
img = cv2.imread(INPUT)
H, W = img.shape[:2]
print(f"Tamano original: {W}x{H}")

# Detectar caras
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=4, minSize=(100, 100))
faces_sorted = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[:3]
print(f"\nCaras detectadas (3 mas grandes): {len(faces_sorted)}")

def sharpen_region(image, x1, y1, x2, y2, strength=2.0, sigma=0.8):
    region = image[y1:y2, x1:x2].copy()
    blurred = cv2.GaussianBlur(region, (0, 0), sigmaX=sigma)
    sharpened = cv2.addWeighted(region, 1.0 + strength, blurred, -strength, 0)
    image[y1:y2, x1:x2] = sharpened
    return image

# Sharpening en ojos+cejas de cada persona
print("\nSharpening ojos+cejas de las 3 personas...")
for i, (x, y, w, h) in enumerate(faces_sorted):
    eye_x1 = x + int(w * 0.10)
    eye_y1 = y + int(h * 0.22)
    eye_x2 = x + int(w * 0.90)
    eye_y2 = y + int(h * 0.55)
    img = sharpen_region(img, eye_x1, eye_y1, eye_x2, eye_y2, strength=2.2, sigma=0.7)
    img = sharpen_region(img, x, y, x + w, y + h, strength=1.0, sigma=1.0)
    print(f"  Cara {i}: sharpened")

# Sharpening global suave
print("Sharpening global suave...")
blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=1.0)
img = cv2.addWeighted(img, 1.4, blurred, -0.4, 0)

# 2-pasos Lanczos para mejor upscale 4x
TARGET_W = 10000  # 60 cm = 23.6 inch -> 10000/23.6 = 424 DPI (excelente)
print(f"\n2-pasos Lanczos a {TARGET_W} ancho...")

# Paso 1: 2x
print(f"  Paso 1: {W}x{H} -> {W*2}x{H*2}")
img = cv2.resize(img, (W*2, H*2), interpolation=cv2.INTER_LANCZOS4)

# Sharpening leve entre pasos
blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=0.8)
img = cv2.addWeighted(img, 1.3, blurred, -0.3, 0)

# Paso 2: final
final_h = int(H * (TARGET_W / W))
print(f"  Paso 2: {W*2}x{H*2} -> {TARGET_W}x{final_h}")
img = cv2.resize(img, (TARGET_W, final_h), interpolation=cv2.INTER_LANCZOS4)

# PIL post-process
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
img_pil = ImageEnhance.Contrast(img_pil).enhance(1.05)
img_pil = ImageEnhance.Color(img_pil).enhance(1.08)
img_pil = ImageEnhance.Sharpness(img_pil).enhance(1.25)
img_pil = img_pil.filter(ImageFilter.UnsharpMask(radius=2.0, percent=130, threshold=3))

# Guardar con DPI 300
print(f"\nGuardando {OUT_PNG}...")
img_pil.save(OUT_PNG, "PNG", dpi=(300, 300), optimize=False)

print(f"Guardando {OUT_JPG}...")
img_pil.save(OUT_JPG, "JPEG", dpi=(300, 300), quality=92, optimize=True)

import os
print(f"\n=== RESULTADO ===")
print(f"Tamano final: {img_pil.size}")
print(f"DPI: 300")
print(f"PNG: {os.path.getsize(OUT_PNG)/1024/1024:.1f} MB")
print(f"JPG: {os.path.getsize(OUT_JPG)/1024/1024:.1f} MB")
print(f"\n45x60 cm (60 long): {TARGET_W/23.6:.0f} DPI")
print(f"45x60 cm (45 short): {final_h/17.7:.0f} DPI")
print(f"A4 21x30: {TARGET_W/11.81:.0f} DPI")
