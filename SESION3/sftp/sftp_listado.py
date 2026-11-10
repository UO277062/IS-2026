"""
Ejercicio 12: conectar por SSH y, con el protocolo SFTP (que va DENTRO de SSH),
listar la carpeta del usuario remoto (SSH ya nos deja en el $HOME, no hace falta chdir).
Uso: python sftp_listado.py [host]
"""
import getpass
import sys
import paramiko

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
usuario = input("Usuario: ")
clave = getpass.getpass("Contraseña: ")

# 1) Conexión SSH normal
c = paramiko.SSHClient()
c.load_system_host_keys()                               # claves de ~/.ssh/known_hosts
c.set_missing_host_key_policy(paramiko.WarningPolicy()) # si es desconocida, avisa
c.connect(HOST, username=usuario, password=clave)

# 2) Abrimos un canal SFTP sobre ese transporte seguro
sftp = c.open_sftp()

# 3) Usamos el objeto sftp
for nombre in sorted(sftp.listdir()):
    datos = sftp.stat(nombre)
    print("%-30s %8d bytes  permisos %s" % (nombre, datos.st_size, oct(datos.st_mode)))

sftp.close()
c.close()
