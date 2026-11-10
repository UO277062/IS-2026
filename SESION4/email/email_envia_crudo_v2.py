"""
Ejercicio 8: como email_envia_crudo.py pero construyendo el mensaje con la
biblioteca email (EmailMessage). Ojo: as_bytes() NO pone el punto final, al
hablar SMTP en crudo hay que añadir nosotros b"\r\n.\r\n".
Con --adjunto añade logoatc.gif (Ejercicio 9).
Uso: python email_envia_crudo_v2.py [servidor] [puerto] [--adjunto]
"""
import socket
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


args = [a for a in sys.argv[1:] if not a.startswith("--")]
server = args[0] if len(args) > 0 else "relay.uniovi.es"
port = int(args[1]) if len(args) > 1 else 25
fromaddr = "uo300499@uniovi.es"
toaddr = "uo300499@uniovi.es"
subject = "Prueba SMTP con la biblioteca email (con tildes: canción)"
data = "Este mensaje lo ha construido email.message.EmailMessage.\nAcentos: áéíóú ñ."

mensaje = email.message.EmailMessage()
mensaje["To"] = toaddr
mensaje["From"] = fromaddr
mensaje["Subject"] = subject
mensaje["Date"] = email.utils.formatdate(localtime=True)
mensaje["Message-ID"] = email.utils.make_msgid()
mensaje.set_content(data)
if "--adjunto" in sys.argv:
    with open("logoatc.gif", "rb") as f:
        mensaje.add_attachment(f.read(), "image", "gif", filename="atc.gif")

s = socket.create_connection((server, port))
RecvReply(s, b"220")
s.sendall(b"HELO is-uo300499\r\n");                   RecvReply(s, b"250")
s.sendall(b"MAIL FROM:<%s>\r\n" % fromaddr.encode()); RecvReply(s, b"250")
s.sendall(b"RCPT TO:<%s>\r\n" % toaddr.encode());     RecvReply(s, b"250")
s.sendall(b"DATA\r\n");                               RecvReply(s, b"354")
s.sendall(mensaje.as_bytes() + b"\r\n.\r\n");         RecvReply(s, b"250")
s.sendall(b"QUIT\r\n");                               RecvReply(s, b"221")
s.close()
print("Correo enviado")
