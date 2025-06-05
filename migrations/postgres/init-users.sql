CREATE DATABASE users_service_db;
CREATE USER users_service_user WITH PASSWORD 'users_service_password';
GRANT ALL PRIVILEGES ON DATABASE users_service_db TO users_service_user;