import socket
from sys import argv

if len(argv) < 2:
    puerto = 9999
else:
    puerto = int(argv[1])


# Función para recibir los 5 bytes completos
def recvall(socket, cantidad):
    datos = ""

    while len(datos) < cantidad:
        parte = socket.recv(cantidad - len(datos))

        if parte == b"":
            return ""

        datos = datos + parte.decode("ascii")

    return datos


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

    continuar = True

    # Bucle de atención al cliente
    while continuar:
        datos = recvall(sd, 5)

        if datos == "":
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False

        elif datos == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False

        else:
            print("Recibido mensaje: %s" % datos)