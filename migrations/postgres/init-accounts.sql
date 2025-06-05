CREATE DATABASE accounts_service_db;
CREATE USER accounts_service_user WITH PASSWORD 'accounts_service_password';
GRANT ALL PRIVILEGES ON DATABASE accounts_service_db TO accounts_service_user;