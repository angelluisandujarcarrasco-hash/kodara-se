"""
Mejora la foto del couple para impresion 13x18 cm a 300+ DPI.
- Sharpening en las caras
- Upscale 2x con Lanczos
- Boost de luz (la foto es muy oscura)
- DPI 300 inyectado
"""
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT = "couple-original.jpg"
OUT_PNG = "couple-enhanced.png"
OUT_JPG = "couple-enhanced.jpg"

print(f"Cargando {INPUT}...")
img = cv2.imread(INPUT)
H, W = img.shape[:2]
print(f"Tamano original: {W}x{H}")

# ==== 1. Boost de luz (la foto es muy oscura) ====
print("Boost de luz (foto oscura)...")
# Convertir a LAB y aumentar L channel
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)
# CLAHE para realzar detalles en zonas oscuras sin quemar
clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
l_clahe = clahe.apply(l)
lab_enhanced = cv2.merge([l_clahe, a, b])
img = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)

# Ligero brillo global tambien
img = cv2.convertScaleAbs(img, alpha=1.05, beta=10)

# ==== 2. Detectar caras y sharpening ====
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
print(f"\nCaras detectadas: {len(faces)}")

def sharpen_region(image, x1, y1, x2, y2, strength=1.5, sigma=1.0):
    region = image[y1:y2, x1:x2].copy()
    blurred = cv2.GaussianBlur(region, (0, 0), sigmaX=sigma)
    sharpened = cv2.addWeighted(region, 1.0 + strength, blurred, -strength, 0)
    image[y1:y2, x1:x2] = sharpened
    return image

for (x, y, w, h) in faces:
    print(f"  Cara en ({x},{y}) {w}x{h} - aplicando sharpening")
    img = sharpen_region(img, x, y, x + w, y + h, strength=1.8, sigma=0.9)

# Sharpening global suave
print("Sharpening global suave...")
blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=1.0)
img = cv2.addWeighted(img, 1.3, blurred, -0.3, 0)

# ==== 3. Upscale 2x con Lanczos ====
TARGET_W = W * 2
TARGET_H = H * 2
print(f"\nUpscale a {TARGET_W}x{TARGET_H} (Lanczos)...")
img = cv2.resize(img, (TARGET_W, TARGET_H), interpolation=cv2.INTER_LANCZOS4)

# ==== 4. Post-process PIL ====
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

img_pil = ImageEnhance.Contrast(img_pil).enhance(1.08)
img_pil = ImageEnhance.Color(img_pil).enhance(1.10)
img_pil = ImageEnhance.Sharpness(img_pil).enhance(1.3)

# Unsharp mask final
img_pil = img_pil.filter(ImageFilter.UnsharpMask(radius=1.5, percent=130, threshold=2))

# DPI 300
print(f"\nGuardando {OUT_PNG} (300 DPI)...")
img_pil.save(OUT_PNG, "PNG", dpi=(300, 300), optimize=False)

print(f"Guardando {OUT_JPG} (300 DPI, q95)...")
img_pil.save(OUT_JPG, "JPEG", dpi=(300, 300), quality=95, optimize=True)

import os
print(f"\n=== RESULTADO ===")
print(f"Tamano final: {img_pil.size}")
print(f"DPI: 300")
print(f"PNG: {os.path.getsize(OUT_PNG)/1024/1024:.1f} MB")
print(f"JPG: {os.path.getsize(OUT_JPG)/1024/1024:.1f} MB")
print(f"\nPara 13x18 cm: {TARGET_W/5.12:.0f} DPI (excelente)")
print(f"Para 18x24 cm: {TARGET_W/7.09:.0f} DPI (excelente)")
print(f"Para 21x30 cm A4: {TARGET_W/8.27:.0f} DPI (excelente)")
