# Sesión 2.1 — Instalación y configuración de infraestructura software para la Web

Resumen práctico de la sesión: instalación y despliegue de Nginx, configuración de sitios web, ejecución de una aplicación Flask con Gunicorn, conexión mediante un proxy inverso y despliegue de MariaDB con almacenamiento persistente.

> Ejecuta los comandos desde la máquina Ubuntu. Los comandos de Docker presuponen que existe una red llamada `pruebas`. Si todavía no existe, créala una sola vez:
>
> ```bash
> docker network create pruebas
> ```

## 1. Estructura de carpetas del proyecto

Crea una carpeta para guardar los ficheros de la práctica:

```bash
mkdir -p ~/sesion2.1
cd ~/sesion2.1

mkdir -p html html2 sitios_nginx configuracion_nginx hola_flask
```

La estructura que iremos completando será:

```text
sesion2.1/
├── html/
│   ├── index.html
│   └── 50x.html
├── html2/
│   └── index.html
├── sitios_nginx/
│   ├── default.conf
│   └── sitio2.conf
├── configuracion_nginx/
│   └── nginx.conf          # Solo si se hace el apartado opcional de seguridad
├── hola_flask/
│   ├── hola_flask.py
│   └── Dockerfile
├── basedatos/              # Datos persistentes de MariaDB; no subir a Git
└── .gitignore
```

El entorno virtual de Python se crea aparte, en `~/flaskenv`, y no dentro del repositorio.

---

## 2. Instalación de Nginx en Ubuntu

### 2.1. Comprobar los puertos antes de instalar

```bash
sudo netstat -4tln
sudo netstat -4tan
sudo lsof -i4 -n -P
```

- `netstat -4tln`: muestra sockets TCP IPv4 que están escuchando.
- `netstat -4tan`: muestra también las conexiones TCP activas.
- `lsof`: permite identificar qué programas están usando las conexiones.

### 2.2. Instalar y comprobar Nginx

```bash
sudo apt install nginx
nginx -V
systemctl status nginx
sudo netstat -4tln
```

Abre en el navegador la IP de la máquina Ubuntu. Debería aparecer la página por defecto de Nginx, servida por el puerto 80.

Directorios importantes de Nginx:

- `/etc/nginx/`: configuración.
- `/var/log/nginx/`: registros o logs.
- `/usr/share/nginx/html/` o `/var/www/html/`: contenido web, según la distribución.

Comprueba cuál de las dos últimas rutas utiliza Ubuntu modificando el `index.html` correspondiente. También puedes consultar las peticiones en `access.log`.

### 2.3. Desinstalar Nginx del sistema

En los siguientes apartados se ejecutará Nginx dentro de Docker, por lo que la práctica propone quitar la instalación del sistema:

```bash
sudo systemctl stop nginx
sudo apt remove nginx
sudo apt autoremove
sudo netstat -4tln
```

---

## 3. Nginx dentro de Docker

### 3.1. Descargar y arrancar la imagen

```bash
docker pull nginx
docker images
docker run -d --rm --network pruebas --name nginx nginx
docker ps
```

El servidor escucha en el puerto 80 **del contenedor**, no en el puerto 80 de Ubuntu. Por eso todavía no se puede acceder a él desde el exterior usando la IP de Ubuntu.

Consulta la IP interna del contenedor:

```bash
docker inspect nginx
```

Prueba desde Ubuntu, sustituyendo la dirección por la IP obtenida:

```bash
wget http://IP_DEL_CONTENEDOR/
wget http://IP_DEL_CONTENEDOR/50x.html
```

### 3.2. Publicar el puerto y montar los ficheros web

Detén el contenedor anterior:

```bash
docker stop nginx
```

Guarda los ficheros descargados en la carpeta `html/` del proyecto. Después, desde la carpeta `html/`, ejecuta:

```bash
cd ~/sesion2.1/html

docker run -d --rm --network pruebas --name nginx \
  -p 80:80 \
  -v "$(pwd)":/usr/share/nginx/html \
  nginx
```

- `-p 80:80`: publica el puerto 80 del contenedor en el puerto 80 de Ubuntu.
- `-v "$(pwd)":/usr/share/nginx/html`: monta la carpeta actual dentro del directorio web de Nginx.

Ahora abre `http://IP_DE_UBUNTU/`. Los cambios que hagas en `html/index.html` se verán al recargar el navegador.

Para consultar las peticiones recibidas:

```bash
docker logs nginx
```

---

## 4. Configuración básica de Nginx y sitios virtuales

### 4.1. Crear la configuración del primer sitio

Desde la carpeta del proyecto:

```bash
cd ~/sesion2.1
```

Crea `sitios_nginx/default.conf` copiando la configuración por defecto que se encuentra dentro del contenedor en `/etc/nginx/conf.d/default.conf`.

La estructura principal de un sitio es:

```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ =404;
    }

    error_page 500 502 503 504 /50x.html;

    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
```

Conceptos importantes:

- `server`: define un sitio virtual.
- `listen`: puerto en el que escucha.
- `server_name`: nombre del servidor.
- `location`: reglas para una ruta.
- `root`: carpeta donde están los ficheros.
- `index`: fichero que se sirve al solicitar un directorio.
- `try_files`: prueba las rutas indicadas; `=404` devuelve un error si no encuentra el fichero.

### 4.2. Arrancar Nginx con la configuración local

Desde `~/sesion2.1`:

```bash
docker run -d --rm --network pruebas --name nginx \
  -p 80:80 \
  -v "$(pwd)/html":/usr/share/nginx/html \
  -v "$(pwd)/sitios_nginx":/etc/nginx/conf.d \
  nginx
```

Se montan dos carpetas: una para el contenido web y otra para los ficheros de configuración.

Prueba `http://IP_DE_UBUNTU/` y una ruta que no exista para comprobar el error 404.

### 4.3. Ejercicio: segundo sitio virtual en el puerto 81

Crea `sitios_nginx/sitio2.conf` a partir de `default.conf`, modificando:

```nginx
listen 81;
root /usr/share/nginx/html2;
```

Crea un `index.html` diferente dentro de `html2/`.

Detén Nginx y vuelve a arrancarlo desde `~/sesion2.1`:

```bash
docker stop nginx

docker run -d --rm --network pruebas --name nginx \
  -p 80:80 -p 81:81 \
  -v "$(pwd)/html":/usr/share/nginx/html \
  -v "$(pwd)/html2":/usr/share/nginx/html2 \
  -v "$(pwd)/sitios_nginx":/etc/nginx/conf.d \
  nginx
```

Comprueba:

- `http://IP_DE_UBUNTU/`: muestra el primer sitio.
- `http://IP_DE_UBUNTU:81/`: muestra el segundo sitio.

Guarda en Git los HTML, las configuraciones y los scripts de lanzamiento.

---

## 5. Seguridad de Nginx (apartado opcional)

Este apartado modifica la configuración global, no los ficheros de los sitios.

Crea la carpeta si no existe y copia la configuración global desde el contenedor:

```bash
mkdir -p ~/sesion2.1/configuracion_nginx
docker cp nginx:/etc/nginx/nginx.conf ~/sesion2.1/configuracion_nginx/nginx.conf
```

Dentro del bloque `http` del fichero `nginx.conf`, añade:

```nginx
server_tokens off;

client_max_body_size 4096k;
client_header_timeout 10;
client_body_timeout 10;
keepalive_timeout 10;
send_timeout 10;
```

Elimina o sustituye el `keepalive_timeout` anterior para no dejar la directiva duplicada.

Para que Nginx utilice esta configuración, monta el fichero en el contenedor al arrancarlo:

```bash
-v "$(pwd)/configuracion_nginx/nginx.conf":/etc/nginx/nginx.conf
```

Este montaje debe añadirse al comando `docker run` de Nginx, ejecutado desde `~/sesion2.1`.

---

## 6. Aplicación web con Flask

### 6.1. Instalar lo necesario y crear un entorno virtual

```bash
sudo add-apt-repository universe
sudo apt install python3-venv

python3 -m venv ~/flaskenv
source ~/flaskenv/bin/activate

pip install wheel
pip install flask
```

El entorno virtual queda en `~/flaskenv`. Para volver a activarlo en otra sesión de terminal:

```bash
source ~/flaskenv/bin/activate
```

Para salir del entorno virtual:

```bash
deactivate
```

### 6.2. Crear la aplicación

Crea `hola_flask/hola_flask.py`:

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hola_flask():
    return '¡Hola Flask!'
```

Desde la carpeta `hola_flask/`, con el entorno virtual activado, ejecuta:

```bash
cd ~/sesion2.1/hola_flask
FLASK_APP=hola_flask.py flask run --host=0.0.0.0
```

Flask escucha por defecto en el puerto 5000. La opción `--host=0.0.0.0` permite aceptar conexiones desde otras máquinas.

Prueba `http://IP_DE_UBUNTU:5000/`.

Para detener el servidor de desarrollo, vuelve a la terminal donde está ejecutándose y pulsa `Ctrl+C`.

### 6.3. Usar Gunicorn como servidor WSGI

Con el entorno virtual activado:

```bash
pip install gunicorn
```

Desde `~/sesion2.1/hola_flask`:

```bash
gunicorn -b 0.0.0.0:5000 -w 4 hola_flask:app
```

- `-b`: dirección IP y puerto donde escucha.
- `-w 4`: crea cuatro procesos trabajadores.
- `hola_flask:app`: módulo Python y variable que contiene la aplicación Flask.

Detén Gunicorn con `Ctrl+C`.

---

## 7. Crear una imagen Docker para Flask y Gunicorn

### 7.1. Crear el Dockerfile

Dentro de `~/sesion2.1/hola_flask/`, crea un fichero llamado `Dockerfile`:

```dockerfile
FROM python:3.7

RUN pip install flask && pip install gunicorn

RUN mkdir /app
COPY hola_flask.py /app

WORKDIR /app

EXPOSE 5000

CMD ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "hola_flask:app"]
```

### 7.2. Construir la imagen

```bash
cd ~/sesion2.1/hola_flask
docker build -t gunicornflask:1.0 .
docker images
```

El punto final indica que Docker debe buscar el `Dockerfile` en la carpeta actual.

### 7.3. Arrancar el contenedor Flask

```bash
docker run --rm -d -p 5050:5000 gunicornflask:1.0
docker ps
```

Accede desde el navegador a:

```text
http://IP_DE_UBUNTU:5050/
```

El puerto 5050 de Ubuntu se redirige al puerto 5000 del contenedor.

Durante el desarrollo también se puede montar la carpeta local sobre `/app`, para que los cambios en el código se reflejen sin reconstruir la imagen:

```bash
cd ~/sesion2.1/hola_flask
docker run --rm -d -p 5050:5000 -v "$(pwd)":/app gunicornflask:1.0
```

---

## 8. Conectar Flask a través de Nginx (proxy inverso)

El objetivo es que Nginx sea el único servicio accesible desde el exterior. Flask/Gunicorn permanecerá dentro de la red Docker `pruebas`, sin publicar su puerto en Ubuntu.

### 8.1. Detener los servicios anteriores

Comprueba los contenedores activos y detén los que correspondan:

```bash
docker ps
docker stop NOMBRE_O_ID
```

Asegúrate de que los puertos anteriores están libres:

```bash
sudo netstat -tpln
```

### 8.2. Arrancar Flask sin publicar el puerto

```bash
docker run -d --rm --name hola-flask \
  --network pruebas \
  gunicornflask:1.0
```

Comprueba:

```bash
docker ps
```

No se utiliza `-p`: el puerto 5000 no queda publicado en el anfitrión. Nginx podrá llegar a Flask porque ambos contenedores estarán en la red `pruebas`.

### 8.3. Configurar Nginx como proxy inverso

Edita `~/sesion2.1/sitios_nginx/default.conf` y añade dentro del bloque `server`:

```nginx
location ~ ^/hola(/?)(.*) {
    resolver 127.0.0.11;
    proxy_pass http://hola-flask:5000/$2;
}
```

Nginx enviará al contenedor `hola-flask` las peticiones que comiencen por `/hola`. Docker proporciona el DNS interno indicado por `127.0.0.11`.

### 8.4. Arrancar Nginx

Desde `~/sesion2.1`:

```bash
docker run -d --rm --network pruebas --name nginx \
  -p 80:80 -p 81:81 \
  -v "$(pwd)/html":/usr/share/nginx/html \
  -v "$(pwd)/html2":/usr/share/nginx/html2 \
  -v "$(pwd)/sitios_nginx":/etc/nginx/conf.d \
  nginx
```

Prueba estas direcciones:

| Dirección | Resultado esperado |
|---|---|
| `http://IP_DE_UBUNTU/` | Página del sitio principal |
| `http://IP_DE_UBUNTU:81/` | Página del segundo sitio |
| `http://IP_DE_UBUNTU/noexisto` | Error 404 generado por Nginx |
| `http://IP_DE_UBUNTU/hola` | Respuesta de Flask |
| `http://IP_DE_UBUNTU/hola/` | Respuesta de Flask |
| `http://IP_DE_UBUNTU/hola/mundo` | Error 404 generado por Flask |

---

## 9. Instalar y ejecutar MariaDB en Docker

### 9.1. Descargar y arrancar MariaDB

```bash
docker pull mariadb
docker images
```

Arranca el servidor en la red `pruebas`:

```bash
docker run --name mariadb \
  -e MYSQL_ROOT_PASSWORD=claveroot \
  --rm --network pruebas -d mariadb
```

Comprueba que está activo:

```bash
docker ps
docker top mariadb
```

MariaDB escucha en el puerto 3306 dentro del contenedor. Como no se ha usado `-p`, el puerto no está publicado en Ubuntu.

> `claveroot` es la contraseña usada en el ejemplo de la práctica. Para un uso real debe elegirse una contraseña segura.

### 9.2. Conectarse a MariaDB desde otro contenedor

Lanza un contenedor temporal con un cliente MariaDB:

```bash
docker run --rm -it --network pruebas mariadb bash
```

Dentro del contenedor, conecta con el servidor:

```bash
mariadb -h mariadb -u root -p
```

Introduce la contraseña configurada (`claveroot`) y, una vez dentro, puedes listar las bases de datos:

```sql
show databases;
```

Sal del cliente con:

```sql
exit
```

Y después sal del contenedor:

```bash
exit
```

---

## 10. Almacenamiento persistente de MariaDB

Si los datos se guardan únicamente dentro del contenedor, se pueden perder cuando este se elimina. Para conservarlos, monta una carpeta del anfitrión en `/var/lib/mysql`.

Desde la raíz del proyecto:

```bash
cd ~/sesion2.1
mkdir -p basedatos
```

Si el contenedor anterior sigue funcionando, detenlo:

```bash
docker stop mariadb
```

Arranca MariaDB montando la carpeta persistente:

```bash
docker run --name mariadb \
  -e MYSQL_ROOT_PASSWORD=claveroot \
  -v "$(pwd)/basedatos":/var/lib/mysql \
  --rm --network pruebas -d mariadb
```

Los datos quedan en `~/sesion2.1/basedatos` y se conservan aunque se detenga y elimine el contenedor. Al volver a arrancarlo con el mismo montaje, MariaDB reutiliza esos datos.

Añade la carpeta de datos a `.gitignore`:

```bash
cd ~/sesion2.1
echo "basedatos/" >> .gitignore
```

**No subas `basedatos/` al repositorio Git.** Contiene los ficheros internos de la base de datos y no forma parte del código de la práctica.

---

## 11. Despliegue del proyecto completo

Esta es la secuencia de arranque del sistema final de la práctica: MariaDB y Flask/Gunicorn quedan dentro de la red Docker `pruebas`; Nginx publica los puertos web y hace de proxy inverso hacia Flask.

Asegúrate de que la red existe:

```bash
docker network create pruebas
```

Si Docker indica que ya existe, no hace falta volver a crearla.

### 11.1. Construir la imagen Flask (cuando cambie el código o el Dockerfile)

```bash
cd ~/sesion2.1/hola_flask
docker build -t gunicornflask:1.0 .
```

### 11.2. Arrancar MariaDB

```bash
cd ~/sesion2.1

docker run --name mariadb \
  -e MYSQL_ROOT_PASSWORD=claveroot \
  -v "$(pwd)/basedatos":/var/lib/mysql \
  --rm --network pruebas -d mariadb
```

### 11.3. Arrancar Flask/Gunicorn

```bash
docker run -d --rm --name hola-flask \
  --network pruebas \
  gunicornflask:1.0
```

### 11.4. Arrancar Nginx

```bash
docker run -d --rm --network pruebas --name nginx \
  -p 80:80 -p 81:81 \
  -v "$(pwd)/html":/usr/share/nginx/html \
  -v "$(pwd)/html2":/usr/share/nginx/html2 \
  -v "$(pwd)/sitios_nginx":/etc/nginx/conf.d \
  nginx
```

### 11.5. Comprobar el despliegue

```bash
docker ps
```

Deberían aparecer los contenedores `mariadb`, `hola-flask` y `nginx`.

Comprueba desde el navegador:

- `http://IP_DE_UBUNTU/`
- `http://IP_DE_UBUNTU:81/`
- `http://IP_DE_UBUNTU/hola`

En esta sesión Flask todavía no consulta MariaDB; esa conexión se trabaja en la sesión siguiente.

---

## 12. Detener los proyectos y volver a arrancarlos

### 12.1. Detener todos los contenedores de esta práctica

Primero comprueba qué está activo:

```bash
docker ps
```

Detén los contenedores por nombre:

```bash
docker stop nginx hola-flask mariadb
```

Si alguno no está ejecutándose, Docker puede indicar que no lo encuentra; no pasa nada. También puedes detenerlos individualmente:

```bash
docker stop nginx
docker stop hola-flask
docker stop mariadb
```

Como se han lanzado con `--rm`, los contenedores se eliminan al detenerlos. **La carpeta `basedatos/` no se elimina**, por lo que los datos de MariaDB permanecen.

Comprueba que no queda ninguno activo:

```bash
docker ps
```

Y revisa los puertos:

```bash
sudo netstat -tpln
```

### 12.2. Volver a desplegar el proyecto

En una nueva sesión de trabajo, no necesitas reconstruir la imagen si no has cambiado el `Dockerfile` ni el código que se copia dentro de la imagen. Basta con ejecutar, desde `~/sesion2.1`, los comandos de arranque de MariaDB, Flask y Nginx del apartado 11.

Si has modificado `hola_flask.py` o el `Dockerfile`, reconstruye primero la imagen:

```bash
cd ~/sesion2.1/hola_flask
docker build -t gunicornflask:1.0 .
cd ~/sesion2.1
```

Después arranca los tres contenedores como se indica en el apartado 11.

### 12.3. Comandos útiles de Docker

| Comando | Para qué sirve |
|---|---|
| `docker ps` | Ver los contenedores activos |
| `docker ps -a` | Ver también los contenedores detenidos |
| `docker images` | Ver las imágenes descargadas o construidas |
| `docker stop nginx` | Detener un contenedor |
| `docker logs nginx` | Consultar los logs |
| `docker top mariadb` | Ver los procesos del contenedor |
| `docker inspect nginx` | Consultar información detallada del contenedor |
| `docker exec -it nginx bash` | Abrir una terminal dentro de un contenedor activo |
| `docker network ls` | Ver las redes Docker |
| `docker network create pruebas` | Crear la red de la práctica |

---

## 13. Ideas clave de la sesión

1. Nginx puede instalarse directamente en Ubuntu o ejecutarse dentro de un contenedor Docker.
2. `-p` publica un puerto del contenedor en el anfitrión; `-v` monta una carpeta o fichero del anfitrión dentro del contenedor.
3. Los sitios virtuales de Nginx se configuran mediante ficheros en `/etc/nginx/conf.d/`.
4. Flask permite desarrollar la aplicación; Gunicorn actúa como servidor WSGI y puede atender varios procesos trabajadores.
5. El `Dockerfile` permite construir una imagen propia con la aplicación Flask y Gunicorn.
6. En el despliegue final, Nginx es el punto de entrada público y redirige `/hola` hacia Flask/Gunicorn.
7. Los contenedores que necesitan comunicarse entre sí se conectan a la misma red Docker (`pruebas`).
8. MariaDB escucha en el puerto 3306 dentro de la red Docker; no es necesario publicar ese puerto al exterior para que otros contenedores accedan.
9. El volumen `basedatos:/var/lib/mysql` (en esta práctica, una carpeta del anfitrión montada con `-v`) permite conservar los datos aunque se elimine el contenedor.
10. Detener contenedores no equivale a borrar los datos persistentes montados desde el anfitrión.
