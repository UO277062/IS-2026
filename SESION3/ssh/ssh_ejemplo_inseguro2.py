"""
Ejercicio 9: WarningPolicy -> acepta la clave pero saca un WARNING con su
fingerprint (hash MD5 de la clave pública, en hexadecimal). Como la lista
de claves conocidas vive en RAM, avisa CADA vez que ejecutas el script.
"""
import getpass
import sys
import time
import paramiko

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
usuario = input("Usuario: ")
clave = getpass.getpass("Contraseña: ")

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.WarningPolicy())   # avisa, pero acepta igualmente
client.connect(HOST, username=usuario, password=clave)
print("Conectado!!")

stdin, stdout, stderr = client.exec_command("ls")
for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
