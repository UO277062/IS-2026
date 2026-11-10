"""
Ejercicio 16 (opcional): resumen (From, Subject, comienzo del cuerpo) de cada
mensaje usando poplib + la biblioteca email, que decodifica bien el Unicode de
las cabeceras y los mensajes multipart.
"""
import getpass
import poplib
import sys
import email
import email.header


def imprime_resumen_mensaje(msg_bytes):
    msg = email.message_from_bytes(msg_bytes)
    remite = msg.get("From", "<desconocido>")
    asunto = msg.get("Subject", "<sin asunto>")
    # Las cabeceras con tildes vienen como =?utf-8?b?...?= y hay que decodificarlas
    remite = email.header.make_header(email.header.decode_header(remite))
    asunto = email.header.make_header(email.header.decode_header(asunto))
    cuerpo = msg.get_payload()
    # Si es multipart, get_payload() es una LISTA de partes: nos quedamos con la 1ª
    if type(cuerpo) == list:
        parte_1 = cuerpo[0].get_payload()
        cuerpo = "---Multipart. Parte 1\n" + parte_1
    print("From:", remite)
    print("Subject:", asunto)
    print(cuerpo[:500])
    if len(cuerpo) > 500:
        print("...[omitido]")
    print("-" * 80)


server = sys.argv[1] if len(sys.argv) > 1 else "pop.gmail.com"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 995
username = input("Usuario: ")
password = getpass.getpass("Contraseña (de aplicación): ")

pop3_mail = poplib.POP3_SSL(server, port)
pop3_mail.user(username)
pop3_mail.pass_(password)
num, _ = pop3_mail.stat()
for n in range(1, num + 1):
    _, lineas, _ = pop3_mail.retr(n)
    # poplib da una lista de líneas: las unimos con \r\n para tener el mensaje en bytes
    imprime_resumen_mensaje(b"\r\n".join(lineas))
pop3_mail.quit()
