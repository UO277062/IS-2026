"""
Ejercicio 7: enviar un correo hablando SMTP "a pelo" por un socket TCP.
Solo funciona desde la red de Uniovi (relay.uniovi.es rechaza conexiones de fuera).
Uso: python email_envia_crudo.py [servidor] [puerto]
"""
import socket
import sys


def RecvReply(sock, codigo):
    """Recibe la respuesta del servidor y comprueba que empieza por el código esperado."""
    respuesta = sock.recv(1024)
    # Respuestas multilínea (p.ej. al EHLO): "250-..." = sigue, "250 ..." = última.
    # Si aún no ha llegado la última línea, seguimos leyendo.
    while not respuesta.endswith(b"\r\n") or respuesta.split(b"\r\n")[-2][3:4] == b"-":
        respuesta += sock.recv(1024)
    print("S:", respuesta.decode(errors="replace").rstrip())
    if respuesta[:3] != codigo:
        print("ERROR: esperaba %s y recibí %s" % (codigo.decode(), respuesta[:3].decode()))
        sys.exit(1)


def enviar(sock, comando):
    print("C:", comando.rstrip().decode())
    sock.sendall(comando)


server = sys.argv[1] if len(sys.argv) > 1 else "relay.uniovi.es"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 25
fromaddr = "uo300499@uniovi.es"
toaddr = "uo300499@uniovi.es"
subject = "Prueba SMTP en crudo"
data = "Hola, este correo lo ha enviado un script de Python hablando SMTP directamente."

# Mensaje "artesanal": cabeceras, línea en blanco (\r\n\r\n), cuerpo y "\r\n.\r\n" final
message = """To: %s
From: %s
Subject: %s\r\n\r\n%s\r\n.\r\n""" % (toaddr, fromaddr, subject, data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
RecvReply(s, b"220")                                   # saludo del servidor

enviar(s, b"HELO is-uo300499\r\n");                   RecvReply(s, b"250")
enviar(s, b"MAIL FROM:<%s>\r\n" % fromaddr.encode()); RecvReply(s, b"250")
enviar(s, b"RCPT TO:<%s>\r\n" % toaddr.encode());     RecvReply(s, b"250")
enviar(s, b"DATA\r\n");                               RecvReply(s, b"354")
enviar(s, message.encode("utf-8"));                   RecvReply(s, b"250")
enviar(s, b"QUIT\r\n");                               RecvReply(s, b"221")
s.close()
print("Correo enviado")
