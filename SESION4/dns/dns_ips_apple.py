"""
Ejercicio 5: mostrar TODAS las IPs (registros A) de apple.com.
La respuesta de resolve() se puede recorrer con un for (una entrada por registro).
"""
import dns.resolver

respuesta = dns.resolver.resolve("apple.com", "A")
for registro in respuesta:
    print(registro.address)
