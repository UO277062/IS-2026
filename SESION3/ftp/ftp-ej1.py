"""
Ejercicio 16 (opcional): entrar en un servidor FTP, ir a "carpeta" y listar con LIST.
FTP usa DOS conexiones TCP: una de CONTROL (comandos/respuestas, puerto 21) y otra
de DATOS (por donde llega el listado). Lo que llega por la de datos lo recibimos
con un CALLBACK, que ftplib llama por cada línea.
Uso: python ftp-ej1.py [host] [puerto]
"""
import ftplib
import getpass
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PUERTO = int(sys.argv[2]) if len(sys.argv) > 2 else 21

lista = []


def acumular(linea):
    """Callback: se llama una vez por cada línea recibida por el canal de datos."""
    lista.append(linea)


usuario = input("Usuario: ")
clave = getpass.getpass("Clave? ")
f = ftplib.FTP()
f.connect(HOST, PUERTO)        # Conecta al servidor
f.login(usuario, clave)        # Envía comandos USER y PASS
f.cwd("carpeta")               # Envía comando CWD

lista = []
resp = f.retrlines("LIST", acumular)   # LIST + callback

print("Respuesta del protocolo: ", resp)
print("Contenidos de la carpeta remota:")
for l in lista:
    print(l)
f.quit()
