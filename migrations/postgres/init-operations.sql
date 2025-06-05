CREATE DATABASE operations_service_db;
CREATE USER operations_service_user WITH PASSWORD 'operations_service_password';
GRANT ALL PRIVILEGES ON DATABASE operations_service_db TO operations_service_user;