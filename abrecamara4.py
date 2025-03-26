import cv2
import time
import numpy as np

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Configuración de la cámara
cap.set(3, 640)  # Ancho
cap.set(4, 480)  # Alto

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

    # Si se detecta un contorno grande (movimiento significativo), tomamos la foto
    for contour in contours:
        if cv2.contourArea(contour) > motion_threshold:  # Si el área del contorno es mayor que el umbral
            # Comprobar si han pasado al menos 5 segundos desde la última foto
            if time.time() - last_photo_time > photo_delay:
                # Guardar la foto
                timestamp = int(time.time())  # Usar el tiempo actual para nombrar el archivo
                filename = f"foto_{timestamp}.jpg"
                cv2.imwrite(filename, frame)
                print(f"Foto tomada y guardada como {filename}")

                # Actualizar el tiempo de la última foto tomada
                last_photo_time = time.time()
                break  # Tomar solo una foto por movimiento

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
