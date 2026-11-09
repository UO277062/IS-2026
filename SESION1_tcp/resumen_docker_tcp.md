# Despliegue TCP con Docker

Resumen de comandos para lanzar el servidor y el cliente del ejercicio
`oche`.

## 1. Crear la red Docker

Solo hay que hacerlo una vez. Si la red ya existe, no hace falta
repetirlo.

``` bash
docker network create pruebas
```

## 2. Lanzar el servidor dentro de la red

Esta opción permite que otros contenedores de la red `pruebas` se
conecten al servidor por su nombre (`servidor_oche`).

``` bash
docker run -d --rm --network pruebas --name servidor_oche -v $(pwd):/app \
  python:3.7 python /app/tcp_servidor5_oche_readline.py
```

## 3. Lanzar el cliente desde otro contenedor

El cliente se conecta al servidor usando su nombre y el puerto interno
`9999`.

``` bash
docker run --rm --network pruebas -v $(pwd):/app \
  python:3.7 python /app/tcp_cliente5_oche_readline.py servidor_oche 9999
```

## 4. Exponer el servidor para aceptar conexiones desde fuera

Primero, detener el servidor anterior:

``` bash
docker stop servidor_oche
```

Como se lanzó con `--rm`, el contenedor se elimina automáticamente al
detenerlo.

Ahora lanzar el servidor publicando el puerto `9999` del contenedor en
el puerto `9090` de Ubuntu:

``` bash
docker run -d --rm -p 9090:9999 --network pruebas \
  --name servidor_oche -v $(pwd):/app \
  python:3.7 python /app/tcp_servidor5_oche_readline.py
```

Comprobar que está funcionando y que aparece el mapeo de puertos:

``` bash
docker ps
```

Debe aparecer algo parecido a:

``` text
0.0.0.0:9090->9999/tcp
```

## 5. Conectar desde Ubuntu (fuera de Docker)

Ejecutar el cliente directamente en la máquina anfitriona:

``` bash
python3 tcp_cliente5_oche_readline.py localhost 9090
```

Desde otro equipo de la red, usar la IP de Ubuntu y el puerto `9090`:

``` bash
python3 tcp_cliente5_oche_readline.py IP_DE_UBUNTU 9090
```

## 6. Detener el servidor

``` bash
docker stop servidor_oche
```

Al usar `--rm`, Docker elimina el contenedor al detenerlo.

## Ideas clave

-   `--network pruebas`: conecta el contenedor a la red Docker
    `pruebas`.
-   `--name servidor_oche`: permite que otros contenedores de esa misma
    red localicen el servidor por su nombre.
-   `-p 9090:9999`: publica el puerto `9999` del contenedor en el puerto
    `9090` de Ubuntu.
-   `--rm`: elimina automáticamente el contenedor cuando se detiene.
-   En una conexión entre contenedores de la misma red se usa
    `servidor_oche:9999`.
-   Desde Ubuntu se usa `localhost:9090`; desde otro equipo, la IP de
    Ubuntu y el puerto `9090`.

**Nota sobre VirtualBox:** con adaptador puente se puede acceder usando
la IP de Ubuntu. Con NAT hay que configurar una redirección de puertos
en VirtualBox hacia el puerto `9090` de Ubuntu.
