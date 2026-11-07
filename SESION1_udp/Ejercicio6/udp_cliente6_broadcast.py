import socket
from sys import argv

if len(argv) < 2:
    broadcast = "255.255.255.255"
else:
    broadcast = argv[1]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Activamos el modo broadcast
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Enviamos el mensaje de búsqueda
mensaje = "BUSCANDO HOLA"
s.sendto(mensaje.encode("utf-8"), (broadcast, 12345))

print("Buscando servidores HOLA...")

primerServidor = ""

# Esperamos respuestas de los servidores
while True:
    try:
        s.settimeout(3)

        respuesta, origen = s.recvfrom(1024)

        respuesta = respuesta.decode("utf-8")

        if respuesta == "IMPLEMENTO HOLA":
            print("Servidor encontrado:", origen[0])

            if primerServidor == "":
                primerServidor = origen[0]

    except socket.timeout:
        break

# Si hemos encontrado algún servidor, probamos el servicio
if primerServidor != "":
    print("Probando servidor:", primerServidor)

    mensaje = "HOLA"
    s.sendto(mensaje.encode("utf-8"), (primerServidor, 12345))

    respuesta, origen = s.recvfrom(1024)

    print("Respuesta del servidor:", respuesta.decode("utf-8"))

else:
    print("No se ha encontrado ningún servidor")

s.close()