"""
Ejercicio 13: leer correo de Gmail con POP3 "a pelo" (pop.gmail.com:995, SSL directo).
POP3 responde "+OK ..." o "-ERR ...".  Estados: AUTHORIZATION -> TRANSACTION -> UPDATE
Uso: python email_pop3_recibe_crudo.py [servidor] [puerto]
"""
import getpass
import socket
import ssl
import sys
import email
import email.header


def RecvReply(sock):
    respuesta = sock.recv(1024)
    print("S:", respuesta.decode(errors="replace").rstrip()[:200])
    if respuesta[:3] != b"+OK":
        print("ERROR: el servidor no respondió +OK")
        sys.exit(1)
    return respuesta


def recibir_multilinea(sock, inicio=b""):
    """Las respuestas multilínea (RETR, LIST, TOP) acaban en una línea con solo un punto."""
    datos = inicio
    while not datos.endswith(b"\r\n.\r\n"):
        trozo = sock.recv(4096)
        if not trozo:
            break
        datos += trozo
    return datos


server = sys.argv[1] if len(sys.argv) > 1 else "pop.gmail.com"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 995
username = input("Usuario: ")
password = getpass.getpass("Contraseña (de aplicación): ")

# En POP3S el TLS se negocia NADA MÁS conectar (no hay STARTTLS como en SMTP:587)
s = socket.socket()
s.connect((server, port))
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)
RecvReply(sc)                                         # bienvenida

sc.sendall(b"USER %s\r\n" % username.encode());  RecvReply(sc)
sc.sendall(b"PASS %s\r\n" % password.encode());  RecvReply(sc)   # -> TRANSACTION

sc.sendall(b"STAT\r\n")
stat = RecvReply(sc)                     # "+OK <num_mensajes> <bytes_totales>"
num_mensajes = int(stat.split()[1])
print("Hay %d mensajes" % num_mensajes)

if num_mensajes > 0:
    sc.sendall(b"RETR 1\r\n")
    datos = recibir_multilinea(sc, sc.recv(4096))
    primera_linea, contenido = datos.split(b"\r\n", 1)
    print("S:", primera_linea.decode())
    contenido = contenido[:-len(b".\r\n")]          # quitamos el punto final
    msg = email.message_from_bytes(contenido)
    print("Subject:", email.header.make_header(email.header.decode_header(msg.get("Subject", ""))))
    print("From:   ", email.header.make_header(email.header.decode_header(msg.get("From", ""))))

sc.sendall(b"QUIT\r\n")                  # -> UPDATE (se borran los marcados con DELE)
RecvReply(sc)
sc.close()
