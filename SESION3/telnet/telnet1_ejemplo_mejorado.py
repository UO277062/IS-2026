"""
Ejercicio 1 (mejorado): igual que telnet1_ejemplo.py pero usando read_until()
para DESCARTAR el mensaje de bienvenida y quedarnos solo con la salida del ls.
Truco: el prompt del shell remoto termina en "$ ".
"""
import getpass
import sys
import telnetlib

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
user = input("Usuario remoto: ")
password = getpass.getpass()

tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(user.encode("ascii") + b"\n")
tn.read_until(b"Password: ")
tn.write(password.encode("ascii") + b"\n")

# 1) Leemos y TIRAMOS todo hasta el primer prompt (bienvenida, motd...)
tn.read_until(b"$ ", timeout=10)

# 2) Enviamos el comando y leemos hasta el siguiente prompt
tn.write(b"ls /home\n")
salida = tn.read_until(b"$ ", timeout=10).decode("utf-8")

tn.write(b"exit\n")
tn.close()

# La primera línea es el eco del comando y la última el prompt: las quitamos
lineas = salida.splitlines()
print("\n".join(lineas[1:-1]))
