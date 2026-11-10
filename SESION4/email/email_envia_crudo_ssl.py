"""
Ejercicio 11: enviar por Gmail (smtp.gmail.com:587) en crudo, con cifrado y login:
  EHLO -> STARTTLS (220) -> negociar TLS -> EHLO otra vez -> AUTH LOGIN (334)
  -> usuario en base64 (334) -> contraseña en base64 (235) -> MAIL/RCPT/DATA/QUIT
La "contraseña" es una CONTRASEÑA DE APLICACIÓN de Google, no la normal.
Uso: python email_envia_crudo_ssl.py [servidor] [puerto]
"""
import base64
import getpass
import socket
import ssl
import sys
import email.message, email.utils


def RecvReply(sock, codigo):
    respuesta = sock.recv(1024)
    # Respuestas multilínea (p.ej. al EHLO): "250-..." = sigue, "250 ..." = última.
    # Si aún no ha llegado la última línea, seguimos leyendo.
    while not respuesta.endswith(b"\r\n") or respuesta.split(b"\r\n")[-2][3:4] == b"-":
        respuesta += sock.recv(1024)
    print("S:", respuesta.decode(errors="replace").rstrip())
    if respuesta[:3] != codigo:
        print("ERROR: esperaba %s y recibí %s" % (codigo.decode(), respuesta[:3].decode()))
        sys.exit(1)


server = sys.argv[1] if len(sys.argv) > 1 else "smtp.gmail.com"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 587

username = input("Usuario (tu dirección de gmail): ")
password = getpass.getpass("Contraseña (de aplicación): ")
toaddr = input("Destinatario: ")
fromaddr = username

mensaje = email.message.EmailMessage()
mensaje["To"] = toaddr
mensaje["From"] = fromaddr
mensaje["Subject"] = "Prueba SMTP en crudo con STARTTLS"
mensaje["Date"] = email.utils.formatdate(localtime=True)
mensaje["Message-ID"] = email.utils.make_msgid()
mensaje.set_content("Enviado hablando SMTP a mano, cifrado con TLS y autenticado.")

s = socket.create_connection((server, port))
RecvReply(s, b"220")
s.sendall(b"EHLO is-uo300499\r\n")       # EHLO: SMTP extendido, lista extensiones
RecvReply(s, b"250")                     # ... entre ellas debería venir STARTTLS
s.sendall(b"STARTTLS\r\n")
RecvReply(s, b"220")

# A partir de aquí TODO va cifrado: usamos el socket "envuelto" sc
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

sc.sendall(b"EHLO is-uo300499\r\n")      # tras TLS hay que repetir EHLO
RecvReply(sc, b"250")
sc.sendall(b"AUTH LOGIN\r\n")
RecvReply(sc, b"334")
sc.send(base64.b64encode(username.encode("ascii")) + b"\r\n")
RecvReply(sc, b"334")                    # espera la contraseña
sc.send(base64.b64encode(password.encode("utf8")) + b"\r\n")
RecvReply(sc, b"235")                    # 235 = autenticado

sc.sendall(b"MAIL FROM:<%s>\r\n" % fromaddr.encode()); RecvReply(sc, b"250")
sc.sendall(b"RCPT TO:<%s>\r\n" % toaddr.encode());     RecvReply(sc, b"250")
sc.sendall(b"DATA\r\n");                               RecvReply(sc, b"354")
sc.sendall(mensaje.as_bytes() + b"\r\n.\r\n");         RecvReply(sc, b"250")
sc.sendall(b"QUIT\r\n");                               RecvReply(sc, b"221")
sc.close()
print("Correo enviado")
