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

while linea != "FIN":
    linea = input("Ingrese un mensaje (o FIN para terminar): ")

    if linea != "FIN":
        linea = f"{contadorMensajes} -> {linea}"

        timeout = 0.1
        recibido = False

        while not recibido and timeout <= 2:
            s.settimeout(timeout)
            s.sendto(linea.encode(), (host, port))

            try:
                datagrama, origen = s.recvfrom(1024)
                datagrama = datagrama.decode("utf-8")

                if datagrama == f"OK {contadorMensajes}":
                    print("Recibida confirmación")
                    recibido = True
                else:
                    print("Confirmación no esperada:", datagrama)

            except socket.timeout:
                print("ERROR. El datagrama de confirmación no llega")
                timeout *= 2

        if recibido:
            contadorMensajes += 1
        else:
            print("Puede que el servidor esté caído. Inténtelo más tarde")
            

s.close()