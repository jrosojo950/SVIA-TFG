import cv2
import time
import numpy as np

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Configuración de la cámara
cap.set(3, 1280)  # Ancho
cap.set(4, 720)  # Alto

# Inicializar variables
last_frame = None
motion_threshold = 4000  # Umbral de movimiento (ajustable)
last_photo_time = 0  # Tiempo de la última foto tomada
photo_delay = 5  # Tiempo en segundos entre fotos (ajustable)

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se puede acceder a la cámara.")
        break

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque para reducir el ruido
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # Si no tenemos el primer frame, lo guardamos
    if last_frame is None:
        last_frame = gray
        continue

    # Calcular la diferencia entre el frame actual y el anterior
    frame_diff = cv2.absdiff(last_frame, gray)

    # Umbral para obtener las áreas de movimiento
    _, thresh = cv2.threshold(frame_diff, 50, 255, cv2.THRESH_BINARY)

    # Encontrar contornos en la imagen umbralizada
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si se detecta un contorno grande (movimiento significativo), tomamos las fotos
    for contour in contours:
        if cv2.contourArea(contour) > motion_threshold:  # Si el área del contorno es mayor que el umbral
            if time.time() - last_photo_time > photo_delay:
                print("Movimiento detectado, tomando fotos...")

                # Capturar 3 fotos seguidas
                photos = []
                for i in range(10):
                    ret, photo = cap.read()
                    if ret:
                        photos.append(photo)
                        time.sleep(0.1)  # Pequeña pausa entre fotos

                # Evaluar cuál es la mejor foto
                best_photo = None
                max_edges = 0

                for i, photo in enumerate(photos):
                    # Convertir la foto a escala de grises y aplicar detección de bordes
                    gray_photo = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
                    edges = cv2.Canny(gray_photo, 100, 200)
                    edge_count = cv2.countNonZero(edges)

                    print(f"Foto {i + 1} tiene {edge_count} bordes detectados.")

                    # Seleccionar la foto con más bordes (más nítida)
                    if edge_count > max_edges:
                        max_edges = edge_count
                        best_photo = photo

                # Guardar la mejor foto
                if best_photo is not None:
                    timestamp = int(time.time())  # Usar el tiempo actual para nombrar el archivo
                    filename = f"foto_{timestamp}.jpg"
                    cv2.imwrite(filename, best_photo)
                    print(f"Mejor foto guardada como {filename}")

                # Actualizar el tiempo de la última foto tomada
                last_photo_time = time.time()
                break  # Tomar solo una serie de fotos por movimiento

    # Mostrar la imagen con contornos (opcional)
    cv2.drawContours(frame, contours, -1, (0, 255, 0), 2)
    cv2.imshow('Movimiento Detectado', frame)

    # Esperar por una tecla para salir (por ejemplo, presiona 'q' para salir)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Actualizar el último frame
    last_frame = gray

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
