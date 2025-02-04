#!/bin/bash


MONGO_VOLUME=mongodb_data
APP_NETWORK=app-network

# it will create the mongodb_data volume if it is not there
docker volume create $MONGO_VOLUME

# create a docker network if it is not there
docker network inspect $APP_NETWORK >/dev/null 2>&1 || docker network create --label com.docker.compose.network=app-network $APP_NETWORK

# run the mongodb container if not present
docker ps -a --format '{{.Names}}' | grep -w mongodb >/dev/null 2>&1 || docker run --name mongodb -p 27017:27017 --rm -d \
-e MONGO_INITDB_ROOT_USERNAME=root \
-e MONGO_INITDB_ROOT_PASSWORD=password \
-v $MONGO_VOLUME:/data/db \
--network $APP_NETWORK \
mongo --auth


