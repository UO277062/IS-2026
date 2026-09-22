import socket
from sys import argv

if len(argv) <2:
    host = "localhost"
    port = 8080

else:
    host = argv[1]
    port = int(argv[2])


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



linea = ""

while linea != "FIN":
    linea = input("Ingrese un mensaje ( o FIN para terminar ): ")
    s.sendto(linea.encode() , (host,port) )