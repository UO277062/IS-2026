# Resumen de la práctica 2.2: Aplicaciones web y el protocolo HTTP

## Objetivo y aplicación desarrollada

La práctica desarrolla **Amigos**, una aplicación web para almacenar y
consultar nombres de amigos junto con sus coordenadas geográficas. Se
trabaja con el protocolo HTTP, el patrón MVC, una API REST y el
despliegue de la aplicación mediante contenedores Docker.

Tecnologías utilizadas:

-   **Python y Flask**: lógica de la aplicación web.
-   **MariaDB**: base de datos.
-   **SQLAlchemy y Flask-Migrate**: acceso a datos y migraciones.
-   **Gunicorn**: servidor WSGI para ejecutar Flask en producción.
-   **Nginx**: servidor frontal y proxy inverso.
-   **Docker**: empaquetado y ejecución de los servicios.
-   **HTTPie**: pruebas de las peticiones HTTP a la API.

La arquitectura final se compone de tres contenedores conectados a una
misma red Docker:

1.  `basedatos`: servidor MariaDB.
2.  `amigos`: aplicación Flask ejecutada con Gunicorn.
3.  `nginx`: servidor web que recibe las peticiones y las reenvía a
    Flask.

------------------------------------------------------------------------

## 1. Introducción y preparación del entorno

Se presenta la aplicación que se va a construir y las herramientas
necesarias para desarrollarla y desplegarla.

Se prepara el directorio de trabajo y la red Docker que permitirá la
comunicación entre los contenedores.

``` bash
mkdir -p amigos
docker network create pruebas
```

Si la red ya existe, no es necesario volver a crearla.

## 2. Base de datos MariaDB

Se inicia MariaDB en un contenedor y se configura la base de datos
`amigosdb`, el usuario `amigosuser` y su contraseña. El directorio local
`basedatos` se monta como volumen para conservar los datos aunque se
elimine el contenedor.

``` bash
mkdir -p basedatos

docker run --name basedatos \
  -e MYSQL_ROOT_PASSWORD=claveroot \
  -e MYSQL_USER=amigosuser \
  -e MYSQL_DATABASE=amigosdb \
  -e MYSQL_PASSWORD=amigospass \
  -v "$(pwd)/basedatos:/var/lib/mysql" \
  --rm --network pruebas -d mariadb
```

Se comprueba que el contenedor está activo y que la base de datos
responde:

``` bash
docker ps
docker logs basedatos
```

**Importante:** las variables de inicialización de MariaDB se aplican al
crear la base de datos por primera vez sobre un directorio de datos
vacío. Si `basedatos/` ya contiene datos, cambiar esas variables no
cambia automáticamente los usuarios ni las contraseñas existentes.

## 3. Desarrollo de la aplicación Flask y patrón MVC

Se crea la aplicación Flask y se organiza siguiendo el patrón
**Modelo-Vista-Controlador (MVC)**:

-   **Modelo**: representa los datos y permite interactuar con la base
    de datos.
-   **Vista**: presenta la información al usuario mediante plantillas
    HTML.
-   **Controlador**: recibe las peticiones, ejecuta la lógica
    correspondiente y devuelve una respuesta.

Se instalan las dependencias necesarias para Flask, SQLAlchemy, MariaDB
y las migraciones. La aplicación define el modelo de amigo y utiliza
migraciones para crear o modificar la estructura de la base de datos.

Ejemplo de instalación de dependencias:

``` bash
pip install flask flask-sqlalchemy flask-migrate pymysql
```

Se preparan las plantillas HTML y las rutas que permiten mostrar y
gestionar los amigos desde el navegador.

## 4. Organización mediante Blueprints y vistas HTML

Se separan las rutas de la aplicación mediante **Blueprints**, para
organizar mejor las distintas partes del proyecto.

La parte HTML permite acceder a la aplicación desde el navegador y
consultar o gestionar los amigos. Se preparan las plantillas y las rutas
correspondientes.

La ruta de consulta utilizada en las pruebas es:

``` text
/html/amigos
```

## 5. API REST y protocolo HTTP

Se implementa una API REST para gestionar los amigos mediante peticiones
HTTP. Los recursos se consultan o modifican usando los métodos HTTP
adecuados.

  Método     Ruta                           Función
  ---------- ------------------------------ ------------------------------------------
  `GET`      `/api/amigos`                  Obtener la lista de amigos.
  `POST`     `/api/amigos`                  Añadir un amigo.
  `GET`      `/api/amigo/<id>`              Consultar un amigo por su identificador.
  `PUT`      `/api/amigo/<id>`              Modificar un amigo.
  `DELETE`   `/api/amigo/<id>`              Eliminar un amigo.
  `GET`      `/api/amigo/byName/<nombre>`   Buscar un amigo por nombre.

Se instala **HTTPie** para probar los endpoints desde la terminal.
Durante las pruebas se ejecuta el servidor de desarrollo de Flask:

``` bash
export FLASK_APP=lanzar.py
flask run -h 0.0.0.0
```

Ejemplos de pruebas:

``` bash
http GET http://localhost:5000/api/amigos
http GET http://localhost:5000/api/amigo/1
```

Las peticiones `POST` y `PUT` envían datos para crear o modificar
registros; `DELETE` elimina el recurso indicado. La respuesta de la API
utiliza datos JSON.

## 6. Preparación del despliegue con Docker

Se crea un `Dockerfile` para empaquetar la aplicación Flask y sus
dependencias. En el contenedor, Gunicorn ejecuta la aplicación.

Ejemplo de construcción de la imagen:

``` bash
docker build -t amigos:1.0 .
```

También se configura Nginx como proxy inverso. El archivo
`sitios_nginx/default.conf` contiene una configuración equivalente a:

``` nginx
server {
    listen       80;
    server_name  localhost;

    location / {
        resolver 127.0.0.11;
        proxy_pass http://amigos:5000;
    }
}
```

Nginx escucha en el puerto 80 y reenvía las peticiones al servicio
`amigos`, que escucha en el puerto 5000 dentro de la red Docker.

### Arranque de los tres contenedores

Primero se inicia MariaDB; después, Flask/Gunicorn; por último, Nginx.

``` bash
# 1. MariaDB
docker run --name basedatos \
  -e MYSQL_ROOT_PASSWORD=claveroot \
  -e MYSQL_USER=amigosuser \
  -e MYSQL_DATABASE=amigosdb \
  -e MYSQL_PASSWORD=amigospass \
  -v "$(pwd)/basedatos:/var/lib/mysql" \
  --rm --network pruebas -d mariadb

# 2. Aplicación Flask + Gunicorn
docker run --name amigos \
  -e DEPLOYMENT_MODE=production \
  -e DATABASE_URI=mysql+pymysql://amigosuser:amigospass@basedatos/amigosdb \
  --rm -d --network pruebas amigos:1.0

# 3. Nginx
docker run --rm -d --network pruebas --name nginx \
  -v "$(pwd)/sitios_nginx:/etc/nginx/conf.d" \
  -p 80:80 nginx
```

Para comprobar el despliegue:

``` bash
docker ps
docker logs basedatos
docker logs amigos
docker logs nginx
```

Se accede desde el navegador utilizando la IP del equipo donde se
ejecutan los contenedores:

``` text
http://IP_UBUNTU/html/amigos
http://IP_UBUNTU/api/amigos
```

## 7. Ampliación del modelo: campo `device`

Se amplía el modelo de amigo añadiendo el campo `device`, destinado a
guardar información del dispositivo. Se actualizan el modelo, las
migraciones, las vistas HTML y los endpoints de la API para que el nuevo
campo pueda consultarse y modificarse.

Se incorpora también el endpoint:

``` text
GET /api/devices
```

Este endpoint devuelve los valores de dispositivo que estén informados,
evitando los valores nulos o vacíos.

En las plantillas se puede mostrar el campo evitando que aparezca el
texto `None` cuando no tenga valor:

``` jinja2
{{ amigo.device or '' }}
```

Después de modificar la aplicación se construye una nueva versión de la
imagen:

``` bash
docker build -t amigos:2.0 .
```

Al desplegar esta versión, el contenedor `amigos` debe ejecutarse usando
la imagen `amigos:2.0` en lugar de `amigos:1.0`.

## 8. Documentación de la API

Se describe la API mediante una especificación YAML y se utiliza
**Swagger Editor** para visualizar y revisar su documentación.

La documentación recoge los recursos disponibles, las rutas, los métodos
HTTP y los datos que se intercambian.

## 9. Estructura de carpetas y archivos

La organización funcional del proyecto es la siguiente. Los nombres
concretos de algunos módulos pueden depender de cómo se haya seguido la
práctica:

``` text
proyecto/
├── basedatos/                 # Datos persistentes de MariaDB
├── amigos/                    # Código de la aplicación Flask
│   ├── Dockerfile             # Imagen Docker de la aplicación
│   ├── lanzar.py              # Punto de entrada de Flask
│   ├── ...                    # Modelos, controladores y configuración
│   └── ...                    # Plantillas y recursos de la aplicación
└── sitios_nginx/
    └── default.conf           # Configuración del proxy inverso
```

La carpeta `basedatos/` debe mantenerse para conservar la información de
MariaDB. `sitios_nginx/` contiene la configuración que se monta dentro
del contenedor Nginx. El código y el `Dockerfile` de la aplicación se
encuentran en `amigos/`.

------------------------------------------------------------------------

## 10. Guía completa para arrancar y detener el despliegue

### 10.1. Antes de arrancar

Abre una terminal en el directorio que contiene `basedatos/`, `amigos/`
y `sitios_nginx/`.

Comprueba que Docker está disponible:

``` bash
docker --version
docker ps -a
docker network ls
```

Si la red `pruebas` no existe, créala:

``` bash
docker network create pruebas
```

Comprueba que están disponibles las imágenes necesarias:

``` bash
docker images
```

Si has cambiado el código de la aplicación, reconstruye la imagen antes
de arrancar. Para la versión ampliada:

``` bash
cd amigos
docker build -t amigos:2.0 .
cd ..
```

### 10.2. Arranque, en orden

**Paso 1: MariaDB**

``` bash
docker run --name basedatos \
  -e MYSQL_ROOT_PASSWORD=claveroot \
  -e MYSQL_USER=amigosuser \
  -e MYSQL_DATABASE=amigosdb \
  -e MYSQL_PASSWORD=amigospass \
  -v "$(pwd)/basedatos:/var/lib/mysql" \
  --rm --network pruebas -d mariadb
```

**Paso 2: aplicación Flask**

Para la versión 1.0:

``` bash
docker run --name amigos \
  -e DEPLOYMENT_MODE=production \
  -e DATABASE_URI=mysql+pymysql://amigosuser:amigospass@basedatos/amigosdb \
  --rm -d --network pruebas amigos:1.0
```

Para la versión 2.0, utiliza `amigos:2.0` al final del comando:

``` bash
docker run --name amigos \
  -e DEPLOYMENT_MODE=production \
  -e DATABASE_URI=mysql+pymysql://amigosuser:amigospass@basedatos/amigosdb \
  --rm -d --network pruebas amigos:2.0
```

**Paso 3: Nginx**

``` bash
docker run --rm -d --network pruebas --name nginx \
  -v "$(pwd)/sitios_nginx:/etc/nginx/conf.d" \
  -p 80:80 nginx
```

**Paso 4: comprobar el estado**

``` bash
docker ps
```

Deben aparecer los tres contenedores: `basedatos`, `amigos` y `nginx`.

### 10.3. Pruebas de funcionamiento

Desde el navegador:

``` text
http://IP_UBUNTU/html/amigos
http://IP_UBUNTU/api/amigos
```

Desde la terminal, si el puerto 80 está publicado en el equipo local:

``` bash
http GET http://localhost/api/amigos
```

Si algo falla, consulta los registros del contenedor correspondiente:

``` bash
docker logs basedatos
docker logs amigos
docker logs nginx
```

### 10.4. Parada, en orden inverso

Detén primero Nginx, después la aplicación y finalmente MariaDB:

``` bash
docker stop nginx
docker stop amigos
docker stop basedatos
```

Los contenedores de esta práctica se ejecutan con `--rm`, por lo que
Docker los elimina al detenerlos. Esto **no elimina la carpeta
`basedatos/`** ni los datos persistidos en ella.

### 10.5. Qué se conserva y qué no

  -----------------------------------------------------------------------
  Elemento                            Al detener los contenedores
  ----------------------------------- -----------------------------------
  Contenedores `nginx`, `amigos`,     Se eliminan al detenerse porque se
  `basedatos`                         usa `--rm`.

  Datos de MariaDB en `basedatos/`    Se conservan en el disco del
                                      equipo.

  Imágenes Docker (`mariadb`,         Se conservan.
  `nginx`, `amigos:1.0`,              
  `amigos:2.0`)                       

  Red Docker `pruebas`                Se conserva hasta que se elimine
                                      expresamente.

  Código y configuración              Se conservan en sus carpetas
                                      locales.
  -----------------------------------------------------------------------

No borres `basedatos/` si quieres conservar los registros. Tampoco es
necesario eliminar la red o las imágenes para una parada normal.

### 10.6. Comprobaciones y resolución de problemas

-   **No aparece un contenedor en `docker ps`:** revisa si ha terminado
    y consulta `docker ps -a` y sus registros.
-   **La aplicación no conecta con MariaDB:** comprueba que ambos
    contenedores están en la red `pruebas`, que MariaDB está iniciado y
    que `DATABASE_URI` apunta al host `basedatos`.
-   **Nginx no llega a Flask:** comprueba que ambos están en la red
    `pruebas`, que el contenedor se llama `amigos` y que la aplicación
    escucha en el puerto 5000.
-   **El puerto 80 está ocupado:** libera ese puerto o cambia la
    publicación de puertos de Nginx.
-   **No se conservan los datos:** verifica que el volumen
    `$(pwd)/basedatos:/var/lib/mysql` se montó desde el directorio de
    trabajo correcto.

------------------------------------------------------------------------

## 11. Secuencia rápida de trabajo

Para repetir el despliegue sin olvidar el orden:

1.  Situarse en la carpeta raíz del proyecto.
2.  Verificar o crear la red `pruebas`.
3.  Construir la imagen de la aplicación si se han hecho cambios.
4.  Arrancar MariaDB.
5.  Arrancar Flask/Gunicorn.
6.  Arrancar Nginx.
7.  Comprobar los tres contenedores con `docker ps`.
8.  Probar las rutas HTML y API.
9.  Consultar `docker logs` si hay errores.
10. Para apagar, ejecutar `docker stop nginx`, `docker stop amigos` y
    `docker stop basedatos`.

**Idea clave:** arrancar en el orden **base de datos → aplicación →
proxy** y detener en el orden inverso. Mantener la carpeta `basedatos/`
es esencial para no perder los datos entre ejecuciones.
