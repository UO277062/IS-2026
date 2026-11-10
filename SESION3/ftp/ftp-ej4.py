"""
Ejercicio 19 (opcional): descargar TODOS los ficheros de una carpeta remota
(saltándose las subcarpetas). Usamos MLSD para saber qué es fichero y qué carpeta.
Uso: python ftp-ej4.py [host] [puerto] [carpeta_remota]
"""
import ftplib
import getpass
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PUERTO = int(sys.argv[2]) if len(sys.argv) > 2 else 21
CARPETA = sys.argv[3] if len(sys.argv) > 3 else "carpeta"

usuario = input("Usuario: ")
clave = getpass.getpass("Clave? ")
f = ftplib.FTP()
f.connect(HOST, PUERTO)
f.login(usuario, clave)
f.cwd(CARPETA)

lineas = []
f.retrlines("MLSD", lineas.append)

for l in lineas:
    hechos, nombre = l.split(" ", 1)
    if "type=file" not in hechos.lower():   # dir, cdir, pdir -> fuera
        print("Me salto", nombre)
        continue
    with open(nombre, "wb") as f_local:
        f.retrbinary("RETR " + nombre, f_local.write)
    print("Descargado", nombre)
f.quit()
