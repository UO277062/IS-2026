import socket
from sys import argv
import time

if len(argv) < 2:
    puerto = 9999
else:
    puerto = int(argv[1])

# Creación del socket de escucha
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asignarle puerto
s.bind(("", puerto))

# Ponerlo en modo pasivo
s.listen(5)

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")
    sd, origen = s.accept()

    print("Nuevo cliente conectado desde %s, %d" % origen)

    time.sleep(1)

    # Crear un objeto para leer del socket
    entrada = sd.makefile("r")

    continuar = True

    # Bucle de atención al cliente
    while continuar:
        # Recibir la longitud del mensaje
        longitud = entrada.readline()

        if longitud == "":
            print("El cliente ha cerrado la conexión")
            continuar = False

        else:
            # Convertir la longitud a entero
            longitud = int(longitud)

            # Recibir el mensaje completo
            mensaje = entrada.read(longitud)

            # Darle la vuelta al mensaje
            linea = mensaje[::-1]

            # Calcular la longitud de la respuesta
            longitud = "%d\n" % len(bytes(linea, "utf8"))

            # Enviar primero la longitud y después el mensaje
            sd.sendall(bytes(longitud + linea, "utf8"))

    entrada.close()
    sd.close()