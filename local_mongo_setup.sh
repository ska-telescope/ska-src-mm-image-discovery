#!/bin/bash

# it will create the mongodb_data
docker volume create mongodb_data

# create a docker network if is not there
docker network create app-network

# run the mongodb container
docker run --name mongodb -p 27017:27017 --rm -d \
-e MONGO_INITDB_ROOT_USERNAME=root \
-e MONGO_INITDB_ROOT_PASSWORD=password \
-v mongodb_data:/data/db \
--network app-network \
mongo --auth