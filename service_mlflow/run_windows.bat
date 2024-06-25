@echo off

REM Create Docker network
docker network create --driver bridge --opt com.docker.network.bridge.name=autoencoder-net autoencoder-net

REM Start the container
docker compose down
docker compose build
docker compose up -d