"""
Recorta y limpia caras de #25 (abuela) y #26 (mama) para usar como referencias.
"""
import cv2
import sys
sys.stdout.reconfigure(encoding='utf-8')

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def crop_face(input_path, output_path, person_label, expand=1.5):
    img = cv2.imread(input_path)
    H, W = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(80, 80))
    print(f"\n=== {person_label} ({W}x{H}) ===")
    print(f"  Caras detectadas: {len(faces)}")
    if len(faces) == 0:
        return None

    # Usar la cara mas grande
    faces_sorted = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)
    x, y, w, h = faces_sorted[0]
    print(f"  Cara principal: ({x},{y}) size {w}x{h}")

    # Expandir para incluir pelo, cuello, hombros
    ex_w = int(w * expand)
    ex_h = int(h * expand)
    x1 = max(0, x - ex_w // 2)
    y1 = max(0, y - int(ex_h * 0.7))
    x2 = min(W, x + w + ex_w // 2)
    y2 = min(H, y + h + int(ex_h * 1.2))  # mas espacio abajo para hombros

    cropped = img[y1:y2, x1:x2]
    cv2.imwrite(output_path, cropped, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print(f"  Crop guardado: {output_path} {cropped.shape[1]}x{cropped.shape[0]}")
    return output_path

crop_face("n25.jpg", "n25-cara-abuela.jpg", "ABUELA #25", expand=1.4)
crop_face("n26.jpg", "n26-cara-mama.jpg",   "MAMA #26",   expand=1.4)
print("\nDONE")
