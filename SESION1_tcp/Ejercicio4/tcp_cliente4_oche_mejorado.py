import socket
from sys import argv


# Función para recibir una línea completa
def recibe_mensaje(sd):
    buffer = []

    while True:
        byte = sd.recv(1)

        if byte == b"":
            return b""

        buffer.append(byte)

        if len(buffer) >= 2:
            if buffer[-2] == b"\r" and buffer[-1] == b"\n":
                return b"".join(buffer)


if len(argv) < 3:
    host = "localhost"
    puerto = 9999
else:
    host = argv[1]
    puerto = int(argv[2])

# Creación del socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar con el servidor
s.connect((host, puerto))

# Pedir tres líneas al usuario
lineas = []

for i in range(3):
    linea = input("Escribe un mensaje: ")
    lineas.append(linea)

# Enviar los tres mensajes seguidos
for linea in lineas:
    s.sendall(bytes(linea + "\r\n", "utf8"))

# Recibir las tres respuestas
for i in range(3):
    respuesta = recibe_mensaje(s)

    if respuesta == b"":
        print("El servidor ha cerrado la conexión")
        break

    respuesta = respuesta.decode("utf8")

    print("Respuesta del servidor:", repr(respuesta))

# Cerrar el socket
s.close()