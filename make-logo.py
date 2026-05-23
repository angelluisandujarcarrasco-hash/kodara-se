from PIL import Image, ImageDraw

size = 1024
img = Image.new('RGB', (size, size), '#EEEEEE')  # Fondo gris claro (como el original)
draw = ImageDraw.Draw(img)

gold = '#C9A227'

# SHAPE 1: Paralelogramo principal (cuerpo de la K)
# Coordenadas ajustadas mirando la imagen original
shape1 = [
    (430, 195),   # top-left (más a la derecha, más pequeño arriba-izq)
    (820, 215),   # top-right
    (505, 590),   # bottom-right (meets shape 2)
    (210, 830),   # bottom-left (extiende más abajo-izq)
]
draw.polygon(shape1, fill=gold)

# SHAPE 2: Pierna inferior (pentágono)
shape2 = [
    (505, 595),   # top (meets shape 1)
    (835, 740),   # upper right corner
    (835, 880),   # lower right corner
    (530, 880),   # bottom-left
    (455, 765),   # middle-left back up to top
]
draw.polygon(shape2, fill=gold)

img.save('C:/Users/lucie/kodara-se/logo-kodara-boho.png', 'PNG', optimize=True)
print("OK")
