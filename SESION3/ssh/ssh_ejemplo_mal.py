"""
Versión que NO funciona: paramiko por defecto usa RejectPolicy y RECHAZA
cualquier servidor cuya clave pública (host key) no conozca.
Excepción: SSHException: Server 'localhost' not found in known_hosts
(Es lo mismo que cuando PuTTY te enseña el fingerprint, pero sin preguntar.)
"""
import sys
import time
import paramiko

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"

client = paramiko.SSHClient()
client.connect(HOST, username="alumno", password="clave-mal")
print("Conectado!!")

stdin, stdout, stderr = client.exec_command("ls")
for line in stdout:
    print(line.rstrip())
time.sleep(1)
client.close()
