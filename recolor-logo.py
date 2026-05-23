from PIL import Image
import numpy as np

# Cargar el logo original
img = Image.open('C:/Users/lucie/kodara-se/logo-original.png.jpeg').convert('RGB')
arr = np.array(img)

# Colores fuente y destino
# Naranja → Dorado boho
# El fondo es gris claro, lo dejamos igual (o cambiamos a cream)

# Detectar píxeles naranja (R alto, G medio, B bajo)
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]
is_orange = (r > 200) & (g > 80) & (g < 180) & (b < 100)

# Crear nueva imagen con dorado en lugar de naranja
# Dorado boho: #C9A227 = (201, 162, 39)
new_arr = arr.copy()
new_arr[is_orange] = [201, 162, 39]

# Detectar fondo gris claro (todos los canales altos y parecidos)
is_bg = (r > 220) & (g > 220) & (b > 220) & (abs(r.astype(int) - g.astype(int)) < 15) & (abs(g.astype(int) - b.astype(int)) < 15)

# Cambiar fondo a cream linen #FAF3E0 = (250, 243, 224)
new_arr[is_bg] = [250, 243, 224]

# Guardar
new_img = Image.fromarray(new_arr)
new_img.save('C:/Users/lucie/kodara-se/logo-kodara-boho.png', 'PNG', optimize=True)
print(f"OK - tamaño: {new_img.size}")
