import socket
import random
from sys import argv

if len(argv) < 2:
    puerto = 9999 
else:
    puerto = int(argv[1])



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# bind() asigna a un socket previamente creado una dirección y un puerto
s.bind(("",puerto))

while True:
    datagrama, origen = s.recvfrom(1024)
    if random.randint(1,100) <= 50:  # Simular pérdida del 50% de los datagramas
        print("Simulando paquete perdido")
    else:
        print("origen: ",origen , "mensaje:", datagrama.decode("utf-8"))
        
        #Modifica el servidor anterior para que, en caso de que decida no perder el paquete, además de mostrarlo por pantalla envíe al cliente otro datagrama conteniendo el texto “OK”.
        s.sendto("OK".encode(), origen)
        