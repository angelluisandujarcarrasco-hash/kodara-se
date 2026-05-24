"""
Couple v2 - LIMPIO: solo upscale + DPI 300.
SIN tocar luz, color, contraste ni saturacion.
Mantiene el ambiente intimo oscuro original.
"""
import cv2
from PIL import Image
import sys
sys.stdout.reconfigure(encoding='utf-8')

INPUT = "couple-original.jpg"
OUT_PNG = "couple-clean.png"
OUT_JPG = "couple-clean.jpg"

print(f"Cargando {INPUT}...")
img = cv2.imread(INPUT)
H, W = img.shape[:2]
print(f"Tamano original: {W}x{H}")

# Solo upscale 2x con Lanczos (no toca colores ni luz)
TARGET_W = W * 2
TARGET_H = H * 2
print(f"Upscale a {TARGET_W}x{TARGET_H} (Lanczos puro, sin tocar colores)...")
img = cv2.resize(img, (TARGET_W, TARGET_H), interpolation=cv2.INTER_LANCZOS4)

# Guardar con DPI 300 (sin ningun otro cambio)
img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

print(f"Guardando {OUT_PNG} (300 DPI, sin procesado)...")
img_pil.save(OUT_PNG, "PNG", dpi=(300, 300), optimize=False)

print(f"Guardando {OUT_JPG} (300 DPI, q95, sin procesado)...")
img_pil.save(OUT_JPG, "JPEG", dpi=(300, 300), quality=95, optimize=True)

import os
print(f"\n=== RESULTADO ===")
print(f"Tamano final: {img_pil.size}")
print(f"DPI: 300")
print(f"PNG: {os.path.getsize(OUT_PNG)/1024/1024:.1f} MB")
print(f"JPG: {os.path.getsize(OUT_JPG)/1024/1024:.1f} MB")
print(f"\nPara 13x18 cm: {TARGET_W/5.12:.0f} DPI")
print(f"Para 21x30 cm A4: {TARGET_W/8.27:.0f} DPI")
print("\n** Solo upscale, NO modifica luz/color/contraste **")
