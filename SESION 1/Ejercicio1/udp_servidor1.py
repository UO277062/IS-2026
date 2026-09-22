import socket
from sys import argv

if len(argv) <1:
    puerto = 8080 
else:
    puerto = int(argv[1])



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind() asigna a un socket previamente creado una dirección y un puerto
s.bind(("",puerto))

while True:
    datagrama, origen = s.recvfrom(1024)
    #print("Se ha recibido un datagrama desde", origen)
    print("origen: ",origen , "mensaje:", datagrama.decode("utf-8"))