alembic init migrations --template async
alembic -c services/users/alembic.ini revision --autogenerate -m "users"
alembic -c services/users/alembic.ini upgrade head

./scripts/proto.sh