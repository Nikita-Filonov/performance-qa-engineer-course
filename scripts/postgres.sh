#!/bin/bash
set -e

# Настройка переменных окружения
export PGHOST=postgres
export PGUSER=root
export PGPASSWORD=root
export PGDATABASE=postgres

# Ждём готовности Postgres
until psql -c '\q'; do
  echo "Waiting for Postgres..."
  sleep 2
done

# Выполнение init-скриптов
psql -f /docker-entrypoint-initdb.d/init-users.sql
psql -f /docker-entrypoint-initdb.d/init-cards.sql
psql -f /docker-entrypoint-initdb.d/init-accounts.sql
psql -f /docker-entrypoint-initdb.d/init-operations.sql

# Выполнение grant-скриптов — с явным указанием целевых БД
psql -d users_service_db      -f /docker-entrypoint-initdb.d/grant-users.sql
psql -d cards_service_db      -f /docker-entrypoint-initdb.d/grant-cards.sql
psql -d accounts_service_db   -f /docker-entrypoint-initdb.d/grant-accounts.sql
psql -d operations_service_db -f /docker-entrypoint-initdb.d/grant-operations.sql

echo "Initialization complete."
