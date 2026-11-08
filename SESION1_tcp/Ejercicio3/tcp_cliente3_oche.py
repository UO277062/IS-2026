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

continuar = True

while continuar:
    # Pedir una línea al usuario
    linea = input("Escribe un mensaje (FIN para terminar): ")

    if linea == "FIN":
        continuar = False
    else:
        # Enviar el mensaje con el final de línea
        s.sendall(bytes(linea + "\r\n", "utf8"))

        # Recibir la respuesta
        respuesta = s.recv(80)

        # Convertir la respuesta a texto
        respuesta = str(respuesta, "utf8")

        # Mostrar la respuesta
        print("Respuesta del servidor:", respuesta[:-2])

# Cerrar el socket
s.close()