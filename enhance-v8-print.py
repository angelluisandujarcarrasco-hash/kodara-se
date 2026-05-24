"""
Genera v11 PRINT: v8 mejorado para impresion 60x90 cm a ~300 DPI.
- Sharpening en ojos del papa
- Upscale a 10240 px ancho (300 DPI para 90 cm)
- Doble paso Lanczos para mejor calidad en upscale grande
- Guardado PNG (lossless) y JPG (compacto)
"""
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT = "regalo-papa-v8.png"
OUT_PNG = "regalo-papa-v11-print.png"
OUT_JPG = "regalo-papa-v11-print.jpg"

PAPA_FACE = {"x": 1210, "y": 286, "w": 234, "h": 234}
ABUELO_FACE = {"x": 779, "y": 410, "w": 181, "h": 181}
ABUELA_FACE = {"x": 1601, "y": 591, "w": 280, "h": 280}

print(f"Cargando {INPUT}...")
img = cv2.imread(INPUT)
H, W = img.shape[:2]
print(f"Tamano original: {W}x{H}")

# ==== 1. Sharpening localizado en ojos del papa ====
fx, fy, fw, fh = PAPA_FACE["x"], PAPA_FACE["y"], PAPA_FACE["w"], PAPA_FACE["h"]

def sharpen_region(image, x1, y1, x2, y2, strength=2.0, sigma=1.0):
    region = image[y1:y2, x1:x2].copy()
    blurred = cv2.GaussianBlur(region, (0, 0), sigmaX=sigma)
    sharpened = cv2.addWeighted(region, 1.0 + strength, blurred, -strength, 0)
    image[y1:y2, x1:x2] = sharpened
    return image

# Zona ojos+cejas papa
print("Sharpening ojos+cejas del papa (strength 2.0)...")
img = sharpen_region(img, fx + int(fw*0.12), fy + int(fh*0.22),
                          fx + int(fw*0.88), fy + int(fh*0.55),
                          strength=2.0, sigma=0.8)

# Caras de abuelos (mas suave)
for face in [ABUELO_FACE, ABUELA_FACE]:
    x = face["x"]; y = face["y"]
    img = sharpen_region(img, x, y, x + face["w"], y + face["h"], strength=1.1, sigma=1.0)

# ==== 2. Sharpening global pre-upscale ====
print("Sharpening global pre-upscale...")
blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=1.0)
img = cv2.addWeighted(img, 1.4, blurred, -0.4, 0)

# ==== 3. Upscale 2-pasos (mejor calidad para upscales grandes) ====
TARGET_W = 10240  # ~285 DPI para 90 cm
print(f"\nUpscale 2-pasos a {TARGET_W} px ancho...")

# Paso 1: 2x con Lanczos
inter_w = W * 2
inter_h = H * 2
print(f"  Paso 1: {W}x{H} -> {inter_w}x{inter_h} (Lanczos)")
img = cv2.resize(img, (inter_w, inter_h), interpolation=cv2.INTER_LANCZOS4)

# Light sharpening entre pasos para compensar softness
blurred = cv2.GaussianBlur(img, (0, 0), sigmaX=0.8)
img = cv2.addWeighted(img, 1.3, blurred, -0.3, 0)

# Paso 2: final size con Lanczos
final_h = int(H * (TARGET_W / W))
print(f"  Paso 2: {inter_w}x{inter_h} -> {TARGET_W}x{final_h}")
img = cv2.resize(img, (TARGET_W, final_h), interpolation=cv2.INTER_LANCZOS4)

# ==== 4. Post-process via PIL ====
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Boost final
img_pil = ImageEnhance.Contrast(img_pil).enhance(1.05)
img_pil = ImageEnhance.Color(img_pil).enhance(1.08)
img_pil = ImageEnhance.Sharpness(img_pil).enhance(1.25)

# Unsharp mask final
img_pil = img_pil.filter(ImageFilter.UnsharpMask(radius=2.0, percent=130, threshold=3))

# DPI metadata para impresion
print(f"\nGuardando {OUT_PNG} con DPI=300...")
img_pil.save(OUT_PNG, "PNG", dpi=(300, 300), optimize=False)

print(f"Guardando {OUT_JPG} calidad 95 con DPI=300...")
img_pil.save(OUT_JPG, "JPEG", dpi=(300, 300), quality=95, optimize=True)

import os
print(f"\n=== RESULTADO ===")
print(f"Tamano final: {img_pil.size}")
print(f"DPI: 300")
print(f"PNG: {os.path.getsize(OUT_PNG)/1024/1024:.1f} MB")
print(f"JPG: {os.path.getsize(OUT_JPG)/1024/1024:.1f} MB")
print(f"\nPara impresion 90x60 cm: {TARGET_W/35.4:.0f} DPI (excelente)")
print(f"Para impresion 60x40 cm: {TARGET_W/23.6:.0f} DPI (excelente)")
