"""
Ejercicio 13: descargar por SFTP todos los FICHEROS (no las carpetas) de una
carpeta remota.
Uso: python sftp_descarga.py host carpeta_remota [carpeta_local]
"""
import getpass
import os
import sys
from stat import S_ISDIR
import paramiko

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
CARPETA_REMOTA = sys.argv[2] if len(sys.argv) > 2 else "."
CARPETA_LOCAL = sys.argv[3] if len(sys.argv) > 3 else "descargas"

usuario = input("Usuario: ")
clave = getpass.getpass("Contraseña: ")

c = paramiko.SSHClient()
c.load_system_host_keys()
c.set_missing_host_key_policy(paramiko.WarningPolicy())
c.connect(HOST, username=usuario, password=clave)
sftp = c.open_sftp()

sftp.chdir(CARPETA_REMOTA)
os.makedirs(CARPETA_LOCAL, exist_ok=True)

for nombre in sftp.listdir():
    # st_mode lleva codificado el tipo de fichero; S_ISDIR nos dice si es carpeta
    if S_ISDIR(sftp.stat(nombre).st_mode):
        print("Me salto la carpeta", nombre)
        continue
    destino = os.path.join(CARPETA_LOCAL, nombre)
    sftp.get(nombre, destino)            # traer fichero remoto -> local
    print("Descargado %s (%d bytes)" % (nombre, os.path.getsize(destino)))

sftp.close()
c.close()
