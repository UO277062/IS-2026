"""
Ejercicio 10: servidores de correo (registros MX) de gmail.com, con sus IPs,
ORDENADOS por preferencia (número más bajo = más prioridad = el MTA lo prueba antes).
"""
import dns.resolver

respuesta = dns.resolver.resolve("gmail.com", "MX")

# Cada registro MX tiene .preference (prioridad) y .exchange (nombre de la máquina)
for mx in sorted(respuesta, key=lambda r: r.preference):
    nombre = mx.exchange.to_text()
    ip = dns.resolver.resolve(nombre, "A")[0].address   # 2ª consulta: nombre -> IP
    print(mx.preference, nombre, ip)
