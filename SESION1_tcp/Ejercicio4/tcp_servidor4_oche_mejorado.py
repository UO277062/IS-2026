import socket
from sys import argv
import time

if len(argv) < 2:
    puerto = 9999
else:
    puerto = int(argv[1])


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

    # Retardo para comprobar la acumulación de mensajes
    time.sleep(1)

    continuar = True

    # Bucle de atención al cliente
    while continuar:
        # Recibir una línea completa
        mensaje = recibe_mensaje(sd)

        if mensaje == b"":
            print("El cliente ha cerrado la conexión")
            continuar = False

        else:
            # Convertir los bytes a texto
            mensaje = mensaje.decode("utf8")

            # Quitar el final de línea
            linea = mensaje[:-2]

            # Darle la vuelta al mensaje
            linea = linea[::-1]

            # Enviar la respuesta con el final de línea
            sd.sendall(bytes(linea + "\r\n", "utf8"))

    sd.close()