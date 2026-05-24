"""
Enhance v4 (mejor versión hasta ahora): sharpening fuerte en ojos de las 3 personas.
NO toca composición, solo mejora detalles.
"""
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT = "familia2-v4-seedream.png"
OUT_PNG = "familia2-v7-eyes.png"
OUT_JPG = "familia2-v7-eyes.jpg"

print(f"Cargando {INPUT}...")
img = cv2.imread(INPUT)
H, W = img.shape[:2]
print(f"Tamano: {W}x{H}")

# Detectar caras
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=4, minSize=(100, 100))
print(f"\nCaras detectadas: {len(faces)}")

# Filtrar caras: ordenar por tamano (las falsas suelen ser chicas)
faces_sorted = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[:3]
print("Las 3 caras mas grandes:")
for i, (x, y, w, h) in enumerate(faces_sorted):
    print(f"  Cara {i}: ({x},{y}) {w}x{h}")

def sharpen_region(image, x1, y1, x2, y2, strength=2.0, sigma=0.8):
    region = image[y1:y2, x1:x2].copy()
    blurred = cv2.GaussianBlur(region, (0, 0), sigmaX=sigma)
    sharpened = cv2.addWeighted(region, 1.0 + strength, blurred, -strength, 0)
    image[y1:y2, x1:x2] = sharpened
    return image

# Para cada cara, sharpening en zona de ojos+cejas
print("\nSharpening fuerte en ojos+cejas de cada persona...")
for i, (x, y, w, h) in enumerate(faces_sorted):
    # Zona ojos+cejas: 22% a 55% del alto, 12% a 88% del ancho
    eye_x1 = x + int(w * 0.10)
    eye_y1 = y + int(h * 0.22)
    eye_x2 = x + int(w * 0.90)
    eye_y2 = y + int(h * 0.55)
    img = sharpen_region(img, eye_x1, eye_y1, eye_x2, eye_y2, strength=2.2, sigma=0.7)
    print(f"  Cara {i}: ojos+cejas sharpened")

    # Tambien sharpening medio en toda la cara
    img = sharpen_region(img, x, y, x + w, y + h, strength=1.0, sigma=1.0)

# Sharpening global suave
print("\nSharpening global suave...")
blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=1.0)
img = cv2.addWeighted(img, 1.4, blurred, -0.4, 0)

# Convert a PIL
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Boost final
img_pil = ImageEnhance.Contrast(img_pil).enhance(1.05)
img_pil = ImageEnhance.Color(img_pil).enhance(1.08)
img_pil = ImageEnhance.Sharpness(img_pil).enhance(1.3)

# Unsharp mask final
img_pil = img_pil.filter(ImageFilter.UnsharpMask(radius=1.5, percent=130, threshold=3))

# DPI 300
print(f"\nGuardando {OUT_PNG} (300 DPI)...")
img_pil.save(OUT_PNG, "PNG", dpi=(300, 300), optimize=False)
img_pil.save(OUT_JPG, "JPEG", dpi=(300, 300), quality=92, optimize=True)

import os
print(f"\n=== RESULTADO ===")
print(f"Tamano final: {img_pil.size}")
print(f"PNG: {os.path.getsize(OUT_PNG)/1024/1024:.1f} MB")
print(f"JPG: {os.path.getsize(OUT_JPG)/1024/1024:.1f} MB")
