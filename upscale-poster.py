import urllib.request
from PIL import Image
import os

# Descargar la imagen original
url = "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_092123_ee56f122-bfd6-417d-bcec-3bd1bf6056e7.png"
src = "C:/Users/lucie/kodara-se/poster-mi-jefa-soy-yo-original.png"
dst = "C:/Users/lucie/kodara-se/poster-mi-jefa-soy-yo.png"

print("Descargando...")
urllib.request.urlretrieve(url, src)

print("Cargando...")
img = Image.open(src)
print(f"Tamaño original: {img.size}")

# Upscale a 4500 x 6000 (suficiente para 300 DPI en todos los tamaños)
# A3 a 300 DPI = 3508 x 4961
# 16x20" a 300 DPI = 4800 x 6000
# Vamos con 4500x6000 que cubre todo
target = (4500, 6000)
print(f"Escalando a {target}...")
img_hi = img.resize(target, Image.LANCZOS)

# Guardar como PNG con DPI metadata
img_hi.save(dst, "PNG", dpi=(300, 300), optimize=True)

# Verificar
print(f"Tamaño nuevo: {img_hi.size}")
print(f"DPI: 300")
print(f"Archivo final: {dst}")
print(f"Tamaño archivo: {os.path.getsize(dst)/1024/1024:.1f} MB")
