import socket
from sys import argv

if len(argv) < 3:
    host = "localhost"
    port = 9999
else:
    host = argv[1]
    port = int(argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

linea = ""
contadorMensajes = 1

s.settimeout(0.1)

while linea != "FIN":
    linea = input("Ingrese un mensaje (o FIN para terminar): ")

    if linea != "FIN":
        linea = f"{contadorMensajes} -> {linea}"
        s.sendto(linea.encode(), (host, port))

        contadorMensajes += 1

        try:
            datagrama, origen = s.recvfrom(1024)
            datagrama = datagrama.decode("utf-8")

            if datagrama == "OK":
                print("Recibida confirmación")
            else:
                print("Recibido datagrama no esperado")

        except socket.timeout:
            print("ERROR. El datagrama de confirmación no llega")

s.close()