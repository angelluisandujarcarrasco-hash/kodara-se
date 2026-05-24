"""
Crop muy cerrado de la cara de mama - solo cara, sin hombros.
Para evitar el filtro NSFW de Seedream.
"""
import cv2
import sys
sys.stdout.reconfigure(encoding='utf-8')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

img = cv2.imread("n26.jpg")
H, W = img.shape[:2]
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
print(f"Caras detectadas: {len(faces)}")

# Tomar la mas grande
faces_sorted = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
x, y, w, h = faces_sorted[0]
print(f"Cara principal: ({x},{y}) {w}x{h}")

# Crop MUY cerrado: solo cara, espacio para pelo arriba, casi nada abajo
margin_top = int(h * 0.6)       # pelo
margin_side = int(w * 0.25)
margin_bottom = int(h * 0.25)   # solo barbilla, NO hombros/cuerpo

x1 = max(0, x - margin_side)
y1 = max(0, y - margin_top)
x2 = min(W, x + w + margin_side)
y2 = min(H, y + h + margin_bottom)

cropped = img[y1:y2, x1:x2]
cv2.imwrite("mama-cara-tight.jpg", cropped, [cv2.IMWRITE_JPEG_QUALITY, 95])
print(f"Crop tight guardado: {cropped.shape[1]}x{cropped.shape[0]}")
