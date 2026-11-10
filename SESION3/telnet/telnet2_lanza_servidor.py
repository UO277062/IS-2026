"""
Ejercicio 2: usar telnet para arrancar remotamente udp_servidor3_con_ok.py
si no está ya en ejecución.

(Mala práctica a propósito: usuario y clave van en el código, lo pide el enunciado.
 Puedes sobreescribir la clave con la variable de entorno CLAVE_TELNET.)
"""
import os
import sys
import time
import telnetlib

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"
USUARIO = os.environ.get("USUARIO_TELNET", "uo300499")
CLAVE = os.environ.get("CLAVE_TELNET", "pon-aqui-tu-clave")
SERVIDOR = "udp_servidor3_con_ok.py"

tn = telnetlib.Telnet(HOST)
tn.read_until(b"login: ")
tn.write(USUARIO.encode() + b"\n")
tn.read_until(b"Password: ")
tn.write(CLAVE.encode() + b"\n")

# Esperamos al prompt: el shell remoto está listo
tn.read_until(b"$", timeout=10)

# ¿Está ya en marcha? Lo miramos en la lista de procesos.
# OJO: la terminal virtual de telnet tiene 80 columnas y "ps -ef" CORTA las
# líneas largas (saldría "udp_servidor3_con_ok" sin el ".py"). Con "ww" ps no
# recorta las líneas.
tn.write(b"ps -efww\n")
respuesta = tn.read_until(b"$", timeout=10).decode("utf-8")

if SERVIDOR in respuesta:
    print("El servidor ya está en ejecución")
    tn.write(b"exit\n")
else:
    print("El servidor NO estaba en ejecución. Lanzándolo...")
    # nohup: que siga vivo al cerrar telnet.  &: que nos devuelva el prompt
    tn.write(("nohup python3 %s &\n" % SERVIDOR).encode())
    time.sleep(1)                 # le damos tiempo a arrancar
    tn.write(b"exit\n")

# Para depuración, mostramos todo lo que quede
print(tn.read_all().decode("utf-8", errors="replace"))
