"""
Crea versiones comprimidas (JPG bajo 1 MB) para que Angel pueda verlas sin error.
"""
from PIL import Image
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

versions = ["regalo-papa-v3.png", "regalo-papa-v4-seedream.png", "regalo-papa-v6-seamless.png"]

for v in versions:
    if not os.path.exists(v):
        print(f"SKIP: {v} no existe")
        continue
    img = Image.open(v).convert("RGB")
    # Redimensionar a 1600 ancho para mantener calidad razonable
    w, h = img.size
    new_w = 1600
    new_h = int(h * (new_w / w))
    img_small = img.resize((new_w, new_h), Image.LANCZOS)
    out = v.replace(".png", "-small.jpg")
    img_small.save(out, "JPEG", quality=85, optimize=True)
    size_kb = os.path.getsize(out) / 1024
    print(f"OK {out} ({new_w}x{new_h}, {size_kb:.0f} KB)")
