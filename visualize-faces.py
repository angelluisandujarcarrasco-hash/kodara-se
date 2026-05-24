"""
Dibuja rectángulos sobre las caras detectadas para verificar visualmente.
"""
import cv2
import sys
sys.stdout.reconfigure(encoding='utf-8')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

img = cv2.imread("regalo-papa-v4-seedream.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Try with more sensitive detection
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(80, 80))
print(f"Caras detectadas (sensitivo): {len(faces)}")
for i, (x, y, w, h) in enumerate(faces):
    print(f"  Cara {i}: ({x},{y}) size {w}x{h}, centro=({x+w//2},{y+h//2})")
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)
    cv2.putText(img, f"#{i}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)

# Resize for display
h, w = img.shape[:2]
scale = 1200 / w
small = cv2.resize(img, (int(w*scale), int(h*scale)))
cv2.imwrite("debug-faces.png", small)
print("\nGuardado debug-faces.png")
