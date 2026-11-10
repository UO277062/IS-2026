"""
Experimento: hablar con el servidor telnet (puerto 23) con un socket "en crudo".
Lo primero que llega NO es el "login:", sino bytes de NEGOCIACIÓN del protocolo.
    FF = IAC (Interpret As Command)   FB=WILL FC=WONT FD=DO FE=DONT
    FF FD 18  ->  "DO 24"  (opción 24 = TERMINAL-TYPE, RFC 1091)
"""
import socket
import sys

HOST = sys.argv[1] if len(sys.argv) > 1 else "localhost"

NOMBRES = {0xFF: "IAC", 0xFB: "WILL", 0xFC: "WONT", 0xFD: "DO", 0xFE: "DONT"}


def mostrar_hex(respuesta):
    """Muestra cada byte de la respuesta en hexadecimal (y su significado telnet)."""
    for byte in respuesta:
        print(hex(byte), NOMBRES.get(byte, ""))


s = socket.socket()
s.connect((HOST, 23))
respuesta = s.recv(1024)
print("Tal cual la muestra python:", respuesta)
print("Byte a byte en hexadecimal:")
mostrar_hex(respuesta)
s.close()
