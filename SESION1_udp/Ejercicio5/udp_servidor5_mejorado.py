import socket
import random
from sys import argv

if len(argv) < 2:
    puerto = 9999
else:
    puerto = int(argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", puerto))

# Guardamos los números de los mensajes ya recibidos
mensajesRecibidos = []

while True:
    datagrama, origen = s.recvfrom(1024)
    mensaje = datagrama.decode("utf-8")

    numero = mensaje.split(" -> ")[0]

    if numero in mensajesRecibidos:
        print("Mensaje duplicado:", mensaje)

    else:
        if random.randint(1, 100) <= 50:
            print("Simulando paquete perdido")
            continue

        print("origen:", origen, "mensaje:", mensaje)

        mensajesRecibidos.append(numero)

    # Enviamos la confirmación tanto si es nuevo como si es duplicado
    confirmacion = f"OK {numero}"
    s.sendto(confirmacion.encode(), origen)