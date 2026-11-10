"""
Ejercicio 1: ejemplo de la documentación de telnetlib, modificado para
listar la carpeta /home del servidor.

OJO: telnetlib se eliminó de la biblioteca estándar en Python 3.13.
En Python 3.14 hay que instalar el "backport":  pip install standard-telnetlib
(ya está instalado en el entorno ~/paramikoenv)
"""
import getpass
import sys
import telnetlib

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
user = input("Usuario remoto: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)          # telnetlib hace la negociación por nosotros

tn.read_until(b"login: ")            # esperamos a que pida el usuario
tn.write(user.encode("ascii") + b"\n")
if password:
    tn.read_until(b"Password: ")     # ... y la contraseña
    tn.write(password.encode("ascii") + b"\n")

tn.write(b"ls /home\n")              # comando remoto
tn.write(b"exit\n")                  # cerramos el shell remoto

# read_all() lee hasta que el servidor cierra la conexión.
# Decodificamos con UTF-8 (codificación de Ubuntu) en vez de ascii
print(tn.read_all().decode("utf-8"))
