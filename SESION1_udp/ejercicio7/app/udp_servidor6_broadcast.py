import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Activamos el modo broadcast
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Escuchamos en el puerto 12345
s.bind(("", 12345))

print("Servidor esperando mensajes...")

while True:
    mensaje, origen = s.recvfrom(1024)

    mensaje = mensaje.decode("utf-8")

    print("Mensaje recibido de", origen[0], ":", mensaje)

    if mensaje == "BUSCANDO HOLA":
        respuesta = "IMPLEMENTO HOLA"
        s.sendto(respuesta.encode("utf-8"), origen)

    elif mensaje == "HOLA":
        respuesta = "HOLA: " + origen[0]
        s.sendto(respuesta.encode("utf-8"), origen)