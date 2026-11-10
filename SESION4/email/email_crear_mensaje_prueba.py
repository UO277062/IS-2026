"""
Crear un mensaje que cumpla el estándar RFC 5322 con la biblioteca email.
La biblioteca añade sola Content-Type, Content-Transfer-Encoding... y codifica
las tildes (en cabeceras usa =?utf-8?...?=, prohibido mandarlas "tal cual").
Con --adjunto añade logoatc.gif (Ejercicio 9 opcional): el mensaje pasa a ser
multipart/mixed y el adjunto va en base64.
"""
import sys
import email.message, email.policy, email.utils

mensaje = email.message.EmailMessage()
mensaje['To'] = 'Desti Natario <destinatario@example.com>'
mensaje['From'] = 'Remi Tente <remitente@example.com>'
mensaje['Subject'] = 'Mensaje de prueba con tildes: camión, año'
mensaje['Date'] = email.utils.formatdate(localtime=True)
mensaje['Message-ID'] = email.utils.make_msgid()
mensaje.set_content("Esto es una prueba. Ñandú, pingüino, acción.")

if "--adjunto" in sys.argv:
    # wget http://www.atc.uniovi.es/estilo_atc/logoatc.gif
    with open("logoatc.gif", "rb") as f:
        gif = f.read()
    mensaje.add_attachment(gif, "image", "gif", filename="atc.gif")

binario = mensaje.as_bytes()
print(binario.decode("utf-8"))
