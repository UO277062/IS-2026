import socket
from sys import argv

if len(argv) < 3:
    host = "localhost"
    puerto = 9999
else:
    host = argv[1]
    puerto = int(argv[2])

# Creación del socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar con el servidor
s.connect((host, puerto))

# Enviar 5 mensajes de 5 bytes
for i in range(5):
    s.sendall("ABCDE".encode("ascii"))

# Enviar mensaje de finalización
s.sendall("FINAL".encode("ascii"))

# Cerrar socket
s.close()