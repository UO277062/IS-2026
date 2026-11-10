"""
Ejercicio 17 (opcional): igual que ftp-ej1 pero con MLSD, que devuelve el
listado en un formato ESTÁNDAR ("type=file;size=20;... nombre") fácil de parsear.
Mostramos solo los nombres y omitimos las pseudo-carpetas "." y "..".
"""
import ftplib
import getpass
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PUERTO = int(sys.argv[2]) if len(sys.argv) > 2 else 21

lista = []


def acumular(linea):
    lista.append(linea)


usuario = input("Usuario: ")
clave = getpass.getpass("Clave? ")
f = ftplib.FTP()
f.connect(HOST, PUERTO)
f.login(usuario, clave)
f.cwd("carpeta")
f.retrlines("MLSD", acumular)

print("--- MLSD tal cual:")
for l in lista:
    print(l)

print("--- Solo los nombres:")
for l in lista:
    if "type=cdir" in l or "type=pdir" in l:   # "." y ".."
        continue
    hechos, nombre = l.split(" ", 1)  # "hecho1;hecho2; nombre": el nombre va tras el espacio
    print(nombre)
f.quit()
