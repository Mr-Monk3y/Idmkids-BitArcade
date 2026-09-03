import serial

conexion = serial.Serial(
    "COM5",
    115200,
    timeout=1
)

print("Micro:bit conectado. Esperando mensajes...")

while True:
    mensaje = conexion.readline().decode().strip()

    if mensaje:
        print("Recibido:", mensaje)