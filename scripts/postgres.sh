#!/bin/bash
set -e

until psql -h postgres -U root -c '\q'; do
  echo "Waiting for Postgres..."
  sleep 2
done

psql -h postgres -U root -f /docker-entrypoint-initdb.d/init-users.sql
psql -h postgres -U root -f /docker-entrypoint-initdb.d/init-cards.sql
psql -h postgres -U root -f /docker-entrypoint-initdb.d/init-accounts.sql
psql -h postgres -U root -f /docker-entrypoint-initdb.d/init-operations.sql

psql -h postgres -U root -d users_service_db -f /docker-entrypoint-initdb.d/grant-users.sql
psql -h postgres -U root -d cards_service_db -f /docker-entrypoint-initdb.d/grant-cards.sql
psql -h postgres -U root -d accounts_service_db -f /docker-entrypoint-initdb.d/grant-accounts.sql
psql -h postgres -U root -d operations_service_db -f /docker-entrypoint-initdb.d/grant-operations.sql

echo "Initialization complete."
