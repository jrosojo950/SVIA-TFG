import cv2
import time
import os
import numpy as np

# Crear la carpeta donde se guardarán las fotos si no existe
photo_folder = "static/fotos"
os.makedirs(photo_folder, exist_ok=True)

# Inicializar la cámara
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Ancho
cap.set(4, 720)  # Alto

# Inicializar variables
last_frame = None
motion_threshold = 5000  # Umbral de movimiento (ajustable)
last_photo_time = 0  # Tiempo de la última foto tomada
photo_delay = 5  # Tiempo en segundos entre fotos (ajustable)

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se puede acceder a la cámara.")
        break

    # Convertir a escala de grises y aplicar desenfoque
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Si no tenemos el primer frame, lo guardamos
    if last_frame is None:
        last_frame = gray
        continue

    # Calcular diferencia con el frame anterior
    frame_diff = cv2.absdiff(last_frame, gray)
    _, thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

    # Encontrar contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > motion_threshold:
            if time.time() - last_photo_time > photo_delay:
                print("Movimiento detectado, tomando fotos...")

                # Capturar 3 fotos seguidas
                photos = []
                for i in range(10):
                    ret, photo = cap.read()
                    if ret:
                        photos.append(photo)
                        time.sleep(0.1)

                # Evaluar la mejor foto
                best_photo = None
                max_edges = 0

                for i, photo in enumerate(photos):
                    gray_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray_photo, 100, 200)
                    edge_count = cv2.countNonZero(edges)

                    if edge_count > max_edges:
                        max_edges = edge_count
                        best_photo = photo

                if best_photo is not None:
                    timestamp = int(time.time())
                    filename = f"static/fotos/foto_{timestamp}.jpg"
                    cv2.imwrite(filename, best_photo)
                    print(f"Mejor foto guardada como {filename}")

                last_photo_time = time.time()
                break  # Tomar solo una foto por detección

    # Mostrar la imagen con contornos (opcional)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    cv2.imshow('Movimiento Detectado', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    last_frame = gray

cap.release()
cv2.destroyAllWindows()
