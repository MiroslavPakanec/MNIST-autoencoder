docker network create --driver bridge --opt com.docker.network.bridge.name=autoencoder-net autoencoder-net
docker compose down
docker compose build
docker compose up -d