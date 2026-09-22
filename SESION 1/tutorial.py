from sys import argv
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(("", 8080))

s.send(b"Este mensaje se envia por el socket")

datagrama, origen = s.revfrom(1024)  # 1024 es el máximo tamaño esperado
print("Se ha recibido un datagrama desde", origen)
print("Contiene lo siguiente:")
print(datagrama.decode("utf-8"))
# Ahora lo devolvemos a modo de eco
s.sendto(datagrama, origen)

texto = s.recv(50)   # Recibimos 50 bytes (maximo)
texto = texto.decode("utf8") # Lo pasamos lo antes posible a cadena
print("Texto recibido:", texto)  # El resto del programa lo trata como cadena

# La variable texto se ha inicializado de algún modo conteniendo un str
# Por ejemplo, se ha leido con input()
enviados = s.send(texto.encode("utf8")) # A la hora de enviarlo lo paso a bytes
# Cuidado que la variable enviados contendrá el número de bytes enviados
# y no el número de caracteres