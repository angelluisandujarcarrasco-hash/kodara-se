"""
Detecta caras en el base AI y en cada foto de referencia.
Imprime las coordenadas para usarlas en el face-swap.
"""
import cv2
import sys
sys.stdout.reconfigure(encoding='utf-8')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(image_path, label):
    img = cv2.imread(image_path)
    if img is None:
        print(f"FAIL: {image_path} no se pudo leer")
        return []
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    print(f"\n=== {label} ({w}x{h}) ===")
    print(f"  Caras detectadas: {len(faces)}")
    for i, (x, y, fw, fh) in enumerate(faces):
        print(f"  Cara {i}: x={x}, y={y}, w={fw}, h={fh}  (centro: {x+fw//2},{y+fh//2})")
    return faces

# Base AI image
detect_faces("regalo-papa-v4-seedream.png", "BASE AI v4-seedream")

# Reference photos
detect_faces("ref-13.jpg", "Papa #13 (close-up smile)")
detect_faces("ref-12.jpg", "Papa #12 (close-up white shirt)")
detect_faces("src-abuelo-cap.jpg", "Abuelo #1 (red cap close)")
detect_faces("src-abuelo-full.jpg", "Abuelo #2 (Angelina full body)")
detect_faces("src-abuela-pink.jpg", "Abuela #6 (pink fuchsia)")
detect_faces("src-abuela-smile.jpg", "Abuela #8 (smiling teal)")
