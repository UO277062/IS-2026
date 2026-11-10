"""
Ejercicio 14: como el anterior, pero muestra Subject y From de TODOS los mensajes.
Usamos "TOP n 0", que devuelve solo las cabeceras (0 líneas de cuerpo): más rápido.
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


def recibir_multilinea(sock):
    datos = b""
    while not datos.endswith(b"\r\n.\r\n"):
        trozo = sock.recv(4096)
        if not trozo:
            break
        datos += trozo
    return datos


def decodifica(cabecera):
    return str(email.header.make_header(email.header.decode_header(cabecera)))


server = sys.argv[1] if len(sys.argv) > 1 else "pop.gmail.com"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 995
username = input("Usuario: ")
password = getpass.getpass("Contraseña (de aplicación): ")

s = socket.create_connection((server, port))
sc = ssl.create_default_context().wrap_socket(s, server_hostname=server)
RecvReply(sc)
sc.sendall(b"USER %s\r\n" % username.encode());  RecvReply(sc)
sc.sendall(b"PASS %s\r\n" % password.encode());  RecvReply(sc)
sc.sendall(b"STAT\r\n")
num_mensajes = int(RecvReply(sc).split()[1])

for n in range(1, num_mensajes + 1):
    sc.sendall(b"TOP %d 0\r\n" % n)
    datos = recibir_multilinea(sc)
    cabeceras = datos.split(b"\r\n", 1)[1][:-len(b".\r\n")]
    msg = email.message_from_bytes(cabeceras)
    print("[%d] From: %s | Subject: %s" % (n, decodifica(msg.get("From", "")),
                                           decodifica(msg.get("Subject", ""))))

sc.sendall(b"QUIT\r\n")
RecvReply(sc)
sc.close()
