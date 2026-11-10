"""
Ejercicio 12: lo mismo que email_envia_crudo_ssl.py pero con smtplib, que se
encarga de todo el protocolo (códigos, base64, punto final...).
set_debuglevel(1) muestra el diálogo C:/S: para que veamos que es lo mismo.
Uso: python email_smtplib.py [servidor] [puerto]
"""
import getpass
import smtplib
import sys
import email.message, email.utils

server = sys.argv[1] if len(sys.argv) > 1 else "smtp.gmail.com"
port = int(sys.argv[2]) if len(sys.argv) > 2 else 587

username = input("Usuario (tu dirección de gmail): ")
password = getpass.getpass("Contraseña (de aplicación): ")
toaddr = input("Destinatario: ")

mensaje = email.message.EmailMessage()
mensaje["To"] = toaddr
mensaje["From"] = username
mensaje["Subject"] = "Prueba con smtplib"
mensaje["Date"] = email.utils.formatdate(localtime=True)
mensaje["Message-ID"] = email.utils.make_msgid()
mensaje.set_content("Este correo lo ha enviado smtplib.")

s = smtplib.SMTP(server, port)
s.set_debuglevel(1)
s.starttls()                     # EHLO + STARTTLS + negociación TLS
s.login(username, password)      # AUTH
s.sendmail(username, [toaddr], mensaje.as_bytes())   # aquí NO hace falta el "."
s.quit()
print("Correo enviado")
