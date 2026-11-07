# AYUDA.TXT – SESIÓN 1.3: PROGRAMACIÓN DE RED CON PYTHON (UDP)

## 1. COMANDOS DOCKER GENERALES

`docker version` → Comprobar que Docker funciona.

`docker images` → Ver las imágenes descargadas.

`docker pull python:3.7` → Descargar la imagen Python 3.7.

`docker ps` → Ver los contenedores en ejecución.

`docker ps -a` → Ver todos los contenedores, incluidos los detenidos.

`docker logs NOMBRE` → Ver los mensajes y errores de un contenedor.

`docker inspect NOMBRE` → Ver toda la información de un contenedor.

`docker stop NOMBRE` → Parar un contenedor.

`docker start NOMBRE` → Volver a arrancar un contenedor detenido.

`docker rm NOMBRE` → Eliminar un contenedor detenido.

`docker container prune` → Eliminar todos los contenedores que hayan quedado detenidos.

`docker exec -it NOMBRE bash` → Entrar en un contenedor que está funcionando.

`exit` → Salir del contenedor.

## 2. EJECUTAR LOS PROGRAMAS UDP (SIN DOCKER)

Desde la carpeta donde están los archivos Python:

**Ejercicio 1**

Servidor:
`python3 udp_servidor1.py`

Cliente:
`python3 udp_cliente1.py`

Por defecto se utiliza localhost y el puerto 9999.

**Ejercicio 2**

Servidor:
`python3 udp_servidor2_simula_perdidas.py`

Cliente:
`python3 udp_cliente2_numera_mensajes.py`

**Ejercicio 3**

Servidor:
`python3 udp_servidor3_con_ok.py`

Cliente:
`python3 udp_cliente3_espera_ok.py`

**Ejercicio 4**

Servidor:
`python3 udp_servidor3_con_ok.py`

Cliente:
`python3 udp_cliente4_reintenta.py localhost 9999`

**Ejercicio 5 (opcional)**

Servidor:
`python3 udp_servidor5_mejorado.py`

Cliente:
`python3 udp_cliente5_mejorado.py`

**Ejercicio 6**

Servidor:
`python3 udp_servidor6_broadcast.py`

Cliente:
`python3 udp_cliente6_broadcast.py 255.255.255.255`

Para ejecutar clientes y servidores en dos terminales diferentes.

## 3. DOCKER – EJERCICIO 7

`docker container prune` → Eliminar los contenedores que hayan quedado detenidos.

`docker network create pruebas` → Crear la red Docker pruebas. Este paso es importante porque los tres servidores tienen que estar conectados a la misma subred.

`docker network ls` → Comprobar que existe la red.

### Lanzar los tres servidores

Desde la carpeta donde está `udp_servidor6_broadcast.py`:

    docker run -d --name servidor1 --network pruebas -v "$(pwd):/app" python:3.7 python /app/udp_servidor6_broadcast.py

    docker run -d --name servidor2 --network pruebas -v "$(pwd):/app" python:3.7 python /app/udp_servidor6_broadcast.py

    docker run -d --name servidor3 --network pruebas -v "$(pwd):/app" python:3.7 python /app/udp_servidor6_broadcast.py

### Comprobar los servidores

`docker ps` → Comprobar que los tres contenedores están funcionando.

`docker inspect servidor1 | grep IPAddress` → Consultar la IP del contenedor.

`docker exec -it servidor1 bash` → Entrar en el contenedor.

`apt-get update` → Actualizar los paquetes.

`apt-get install iproute2` → Instalar la herramienta ip.

`ip addr` → Consultar la IP y la dirección broadcast de la subred.

`exit` → Salir del contenedor.

### Ejecutar el cliente

Desde la carpeta donde está el cliente:

`python3 udp_cliente6_broadcast.py DIRECCION_BROADCAST`

Sustituir DIRECCION_BROADCAST por la dirección obtenida con ip addr.

### Parar los servidores

`docker stop servidor1 servidor2 servidor3`

### Volver a arrancar los servidores detenidos

`docker start servidor1 servidor2 servidor3`

### Eliminar los servidores

`docker rm servidor1 servidor2 servidor3`

### Eliminar la red Docker (cuando ya no se utilice)

`docker network rm pruebas`

## 4. SCRIPTS SHELL DEL EJERCICIO 7

Archivos que hay que crear:

- `udp_docker_lanzar_servidores.sh`
- `udp_docker_lanzar_cliente.sh`

Dar permisos de ejecución:

`chmod +x udp_docker_lanzar_servidores.sh`

`chmod +x udp_docker_lanzar_cliente.sh`

Ejecutar los servidores:

`./udp_docker_lanzar_servidores.sh`

Ejecutar el cliente:

`./udp_docker_lanzar_cliente.sh`

IMPORTANTE: Si los contenedores ya existen, no se pueden crear otra vez con los mismos nombres. Primero hay que arrancarlos con docker start o eliminarlos con docker rm.