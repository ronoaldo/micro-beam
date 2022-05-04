#!/usr/bin/bash

cd $(dirname $0)

echo "Construindo simulador de banco de dados ..."
docker build -t mydb .

echo "Executando container com o simulador ..."
docker kill mydb || true
docker run --name mydb --rm --detach \
    -e POSTGRES_USER=test \
    -e POSTGRES_PASSWORD=secret \
    -e POSTGRES_DB=mydb \
    -p 5432:5432 mydb

echo "Checando a base de dados ..."
sleep 5 # Espera inicialização do banco de dados
pg_isready --dbname=mydb --host=127.0.0.1 --port=5432 --username=test