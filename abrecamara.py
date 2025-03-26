import cv2
import time

# Inicializar la cámara
cap = cv2.VideoCapture(0)

# Configuración de la cámara
cap.set(3, 640)  # Ancho
cap.set(4, 480)  # Alto

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se puede acceder a la cámara.")
        break

    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar bordes con Canny
    edges = cv2.Canny(gray, 100, 200)

    # Mostrar la imagen con bordes detectados
    cv2.imshow('Bordes', edges)

    # Contar la cantidad de píxeles con bordes
    edge_count = cv2.countNonZero(edges)

    # Si la cantidad de bordes es suficiente, toma una foto
    if edge_count > 1000:  # Puedes ajustar este umbral según sea necesario
        # Guardar la foto
        timestamp = int(time.time())  # Usar el tiempo actual para nombrar el archivo
        filename = f"foto_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Foto tomada y guardada como {filename}")

        # Pausar 2 segundos antes de seguir con la siguiente detección
        time.sleep(15)

    # Esperar por una tecla para salir (por ejemplo, presiona 'q' para salir)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
