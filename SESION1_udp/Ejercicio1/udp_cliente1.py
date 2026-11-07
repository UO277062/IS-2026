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
while linea != "FIN":
    linea = input("Ingrese un mensaje (o FIN para terminar): ")

    if linea != "FIN":
        s.sendto(linea.encode(), (host, port))

s.close()