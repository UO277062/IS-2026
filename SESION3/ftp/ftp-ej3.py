"""
Ejercicio 18 (opcional): descargar prueba.txt como prueba-copia.txt con RETR.
En modo binario el callback (f_local.write) se llama por cada BLOQUE recibido.
"""
import ftplib
import getpass
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
PUERTO = int(sys.argv[2]) if len(sys.argv) > 2 else 21

usuario = input("Usuario: ")
clave = getpass.getpass("Clave? ")
f = ftplib.FTP()
f.connect(HOST, PUERTO)
f.login(usuario, clave)
f.cwd("carpeta")

f_local = open("prueba-copia.txt", "wb")         # ¡modo binario "b"!
result = f.retrbinary("RETR prueba.txt",         # Petición del fichero
                      f_local.write)             # Callback por cada bloque
f_local.close()
print(result)
f.quit()
