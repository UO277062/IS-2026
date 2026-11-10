"""
Ejercicio 11: como ssh_ejemplo_seguro.py pero contra el servidor de un COMPAÑERO.
desconocidos) pero antes REGISTRAMOS la clave pública real del servidor.
La clave sale de /etc/ssh/ssh_host_ed25519_key.pub (2º campo, en base64).
"""
import base64
import getpass
import sys
import time
import paramiko

HOST = sys.argv[1] if len(sys.argv) > 1 else "IP-DEL-COMPAÑERO"
# Clave pública ed25519 del COMPAÑERO (que te la pase: cat /etc/ssh/ssh_host_ed25519_key.pub)
CLAVE_PUBLICA_SERVIDOR = b"PEGA-AQUI-LA-CLAVE-DEL-COMPAÑERO"

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
