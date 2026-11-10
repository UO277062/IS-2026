"""
Ejercicio 15: leer correo con poplib (la biblioteca se ocupa del protocolo).
retr(n) devuelve (respuesta, [líneas sin \r\n], tamaño).
Uso: python email_pop3_poplib.py [servidor] [puerto]
"""
import getpass
import poplib
import sys

server = sys.argv[1] if len(sys.argv) > 1 else "pop.gmail.com"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 995
username = input("Usuario: ")
password = getpass.getpass("Contraseña (de aplicación): ")

pop3_mail = poplib.POP3_SSL(server, port)
pop3_mail.set_debuglevel(2)
pop3_mail.user(username)
pop3_mail.pass_(password)

num, total = pop3_mail.stat()
print("Mensajes: %d (%d bytes)" % (num, total))
if num > 0:
    respuesta, lineas, tamano = pop3_mail.retr(1)
    print(respuesta, tamano)
    for linea in lineas:
        print(linea)
pop3_mail.quit()
