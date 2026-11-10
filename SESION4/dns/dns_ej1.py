"""
Ejercicio 4: primer contacto con dnspython (pip install dnspython, en ~/dnsenv o ~/paramikoenv).
NOTA: en dnspython 2.x la función se llama resolve(); query() es la antigua
(sigue existiendo pero está "deprecated"). Hacen lo mismo.
"""
import dns.resolver

respuesta = dns.resolver.resolve("en.wikipedia.org")   # = dns.resolver.query(...)
print(respuesta[0].address)

# Acceso de "bajo nivel": la respuesta completa del servidor, legible...
print(respuesta.response)
# ... y en el formato binario que viaja realmente por la red (curiosidad)
print(respuesta.response.to_wire())
