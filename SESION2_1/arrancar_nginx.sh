#!/bin/bash

docker run --rm -d --network pruebas \
    --name nginx -p 80:80 \
    -v "$(pwd)/html:/usr/share/nginx/html" \
    -v "$(pwd)/sitios_nginx:/etc/nginx/conf.d" \
    nginx
