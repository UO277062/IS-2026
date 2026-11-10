"""
Ejercicio 10: la opción SEGURA. Volvemos a la política por defecto (rechazar
desconocidos) pero antes REGISTRAMOS la clave pública real del servidor.
La clave sale de /etc/ssh/ssh_host_ed25519_key.pub (2º campo, en base64).
"""
import base64
import getpass
import sys
import time
import paramiko

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
# Clave pública ed25519 de MI máquina Ubuntu (cat /etc/ssh/ssh_host_ed25519_key.pub)
CLAVE_PUBLICA_SERVIDOR = b"AAAAC3NzaC1lZDI1NTE5AAAAIMeb2hSA1/zlZWiN0xeQph7u56bIMUaPFkmuNk2ltgBw"

usuario = input("Usuario: ")
clave = getpass.getpass("Contraseña: ")

client = paramiko.SSHClient()
# Sin set_missing_host_key_policy -> RejectPolicy (lo seguro)
key = paramiko.Ed25519Key(data=base64.b64decode(CLAVE_PUBLICA_SERVIDOR))
client.get_host_keys().add(HOST, "ssh-ed25519", key)

client.connect(HOST, username=usuario, password=clave)
print("Conectado!!")

stdin, stdout, stderr = client.exec_command("ls")
for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
