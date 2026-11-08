import socket
from sys import argv

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

# Crear un objeto para leer líneas del socket
entrada = s.makefile("r")

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
    respuesta = entrada.readline()

    if respuesta == "":
        print("El servidor ha cerrado la conexión")
        break

    # Quitar el final de línea
    respuesta = respuesta[:-2]

    print("Respuesta del servidor:", respuesta)

# Cerrar el objeto de lectura y el socket
entrada.close()
s.close()