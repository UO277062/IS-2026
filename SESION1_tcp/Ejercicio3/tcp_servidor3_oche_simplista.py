import socket
from sys import argv

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

    continuar = True

    # Bucle de atención al cliente
    while continuar:
        # Recibir el mensaje
        mensaje = sd.recv(80)

        if mensaje == b"":
            print("El cliente ha cerrado la conexión")
            continuar = False
        else:
            # Convertir los bytes a texto
            mensaje = str(mensaje, "utf8")

            # Quitar el final de línea
            linea = mensaje[:-2]

            # Darle la vuelta al mensaje
            linea = linea[::-1]

            # Enviar la respuesta con el final de línea
            sd.sendall(bytes(linea + "\r\n", "utf8"))

    sd.close()