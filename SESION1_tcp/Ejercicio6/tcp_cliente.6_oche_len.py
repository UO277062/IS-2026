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

# Crear un objeto para leer del socket
entrada = s.makefile("r")

# Bucle para enviar mensajes
continuar = True

while continuar:
    linea = input("Escribe un mensaje (FIN para terminar): ")

    if linea == "FIN":
        continuar = False

    else:
        # Calcular la longitud del mensaje en bytes
        longitud = "%d\n" % len(bytes(linea, "utf8"))

        # Enviar primero la longitud y después el mensaje
        s.sendall(bytes(longitud + linea, "utf8"))

        # Recibir la longitud de la respuesta
        longitud = entrada.readline()

        # Convertir la longitud a entero
        longitud = int(longitud)

        # Recibir la respuesta completa
        respuesta = entrada.read(longitud)

        print("Respuesta del servidor:", respuesta)

# Cerrar el objeto de lectura y el socket
entrada.close()
s.close()