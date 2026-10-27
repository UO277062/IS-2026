sudo docker run --name basedatos \
  -e MYSQL_ROOT_PASSWORD=claveroot \
  -e MYSQL_USER=amigosuser \
  -e MYSQL_DATABASE=amigosdb \
  -e MYSQL_PASSWORD=amigospass \
  -v $(pwd)/basedatos:/var/lib/mysql \
  --rm --network pruebas -d mariadb \

sudo docker run --name amigos \
   -e DEPLOYMENT_MODE=production \
   -e DATABASE_URI=mysql+pymysql://amigosuser:amigospass@basedatos/amigosdb \
   --rm -d --network pruebas amigos:1.0 \

sudo docker run --rm -d --network pruebas --name nginx \
    -v $(pwd)/sitios_nginx:/etc/nginx/conf.d \
    -p 80:80 nginx