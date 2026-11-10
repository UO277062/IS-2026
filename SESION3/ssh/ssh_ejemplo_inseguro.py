"""
Ejercicio 8: AutoAddPolicy -> acepta a ciegas la clave del servidor.
Funciona, pero estamos expuestos a un ataque "man in the middle".
La contraseña se pide por teclado (mejor que dejarla en el código).
"""
import getpass
import sys
import time
import paramiko

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
usuario = input("Usuario: ")
clave = getpass.getpass("Contraseña: ")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # <- la línea nueva
client.connect(HOST, username=usuario, password=clave)
print("Conectado!!")

stdin, stdout, stderr = client.exec_command("ls")
for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
