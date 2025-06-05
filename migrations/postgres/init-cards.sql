CREATE DATABASE cards_service_db;
CREATE USER cards_service_user WITH PASSWORD 'cards_service_password';
GRANT ALL PRIVILEGES ON DATABASE cards_service_db TO cards_service_user;