#!/bin/bash
# Ejercicio 3: resolución ITERATIVA de en.wikipedia.org "a mano" con dig +norecurse
# En cada paso el servidor NO nos da la respuesta final: nos REMITE (referral)
# al siguiente servidor más cercano, y somos NOSOTROS quienes seguimos preguntando.
set -e
NOMBRE=en.wikipedia.org

# NOTA: en mi red de casa el router/operador INTERCEPTA las consultas DNS por
# UDP/53 y contesta él (se nota porque un servidor raíz responde con el flag "ra"
# y SERVFAIL, cosa imposible). Por eso uso +tcp: así sí llego al servidor real.
# En la red de la universidad funciona igual sin +tcp.
D="dig +norecurse +tcp"

echo "### 0) Pregunta iterativa a Google (8.8.8.8): puede contestar desde su CACHÉ"
dig @8.8.8.8 +norecurse $NOMBRE | grep -A3 'ANSWER SECTION' || echo "(sin respuesta en caché)"

echo; echo "### 1) ¿Quiénes son los servidores raíz?  (dig . NS)"
RAIZ=$(dig @8.8.8.8 . NS +short | sort | head -1)
IP_RAIZ=$(dig @8.8.8.8 $RAIZ A +short | head -1)
echo "Servidor raíz elegido: $RAIZ -> $IP_RAIZ"

echo; echo "### 2) Pregunto al RAÍZ por org.  -> me remite a los servidores de .org"
$D @$IP_RAIZ org. NS | sed -n '/AUTHORITY SECTION/,/^$/p' | head -4
TLD=$($D @$IP_RAIZ org. NS | awk '/AUTHORITY SECTION/{f=1;next} f&&/NS/{print $5; exit}')
IP_TLD=$(dig @8.8.8.8 $TLD A +short | head -1)
echo "Servidor de .org elegido: $TLD -> $IP_TLD"

echo; echo "### 3) Pregunto al servidor de .org por wikipedia.org -> me remite a los de Wikipedia"
$D @$IP_TLD wikipedia.org. NS | sed -n '/AUTHORITY SECTION/,/^$/p'
NSW=$($D @$IP_TLD wikipedia.org. NS | awk '/AUTHORITY SECTION/{f=1;next} f&&/NS/{print $5; exit}')
IP_NSW=$(dig @8.8.8.8 $NSW A +short | head -1)
echo "Servidor de wikipedia.org elegido: $NSW -> $IP_NSW"

echo; echo "### 4) Pregunto al servidor AUTORITATIVO de wikipedia.org por $NOMBRE"
$D @$IP_NSW $NOMBRE | grep -E 'flags|IN\s+(A|CNAME)'

echo; echo "### 4b) Es un alias (CNAME): pregunto al mismo servidor por el nombre canónico"
CANON=$($D @$IP_NSW $NOMBRE | awk '/CNAME/ && $1!~/^;/{print $5; exit}')
$D @$IP_NSW $CANON A | grep -E 'flags|IN\s+A'

echo; echo "### 5) Comparación con 'host' (resolución recursiva normal)"
host $NOMBRE
