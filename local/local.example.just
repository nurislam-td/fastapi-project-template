# Example from local justfile
[group: "dev"]
up-db:
    docker compose -f local/docker-compose.yml up -d db
