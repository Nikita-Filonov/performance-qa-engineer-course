alembic init migrations --template async
alembic -c services/users/alembic.ini revision --autogenerate -m "users"
alembic -c services/users/alembic.ini upgrade head

./scripts/proto.sh

docker compose -f docker-compose.ci.yaml up -d
docker compose -f docker-compose.ci.yaml up

docker compose -f docker-compose.ci.yaml --env-file .env.ci up + environment: ENV_FILE=.env.ci
ENV_FILE=.env.ci docker compose --env-file .env.ci -f docker-compose.ci.yaml up