"""
Ejercicio 6 (opcional): conectar con la web de Wikipedia usando getaddrinfo(),
que nos dice QUÉ PARÁMETROS pasar a socket() y connect() (familia IPv4/IPv6,
tipo de socket, protocolo y dirección), en vez de suponerlos nosotros.
"""
import socket

opciones = socket.getaddrinfo("en.wikipedia.org", "www", type=socket.SOCK_STREAM)
for o in opciones:
    print(o)

# Nos quedamos con la primera opción IPv4 (AF_INET)
familia, tipo, proto, canonname, direccion = next(
    o for o in opciones if o[0] == socket.AF_INET)
print("\nConectando por IPv4 a", direccion)

s = socket.socket(familia, tipo, proto)     # los 3 primeros elementos -> socket()
s.connect(direccion)                        # el 5º elemento -> connect()
s.sendall(b"GET / HTTP/1.1\r\nHost: en.wikipedia.org\r\nConnection: close\r\n\r\n")

respuesta = b""
while True:
    datos = s.recv(4096)
    if not datos:
        break
    respuesta += datos
s.close()
# Mostramos solo las cabeceras (Wikipedia redirige / a /wiki/Main_Page, y por HTTP
# plano a HTTPS: veremos un 301)
print(respuesta.split(b"\r\n\r\n")[0].decode())

# Por IPv6 sería igual con la opción AF_INET6 (si tu red lo soporta)
