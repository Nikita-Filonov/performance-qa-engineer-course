from pydantic_settings import BaseSettings, SettingsConfigDict

from libs.config.grpc import GRPCServerConfig, GRPCClientConfig
from libs.config.http import HTTPServerConfig, HTTPClientConfig
from libs.config.postgres import PostgresConfig
from libs.config.redis import RedisClientConfig
from libs.config.s3 import S3ClientConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='allow',
        env_file='.env',
        env_file_encoding='utf-8',
        env_nested_delimiter='.'
    )

    users_http_server: HTTPServerConfig
    users_http_client: HTTPClientConfig
    users_grpc_server: GRPCServerConfig
    users_grpc_client: GRPCClientConfig
    users_postgres_database: PostgresConfig

    cards_http_server: HTTPServerConfig
    cards_http_client: HTTPClientConfig
    cards_grpc_server: GRPCServerConfig
    cards_grpc_client: GRPCClientConfig
    cards_postgres_database: PostgresConfig

    gateway_http_server: HTTPServerConfig
    gateway_grpc_server: GRPCServerConfig
    gateway_redis_client: RedisClientConfig

    payments_http_client: HTTPClientConfig
    payments_grpc_client: GRPCClientConfig
    payments_system_enabled: bool

    accounts_http_server: HTTPServerConfig
    accounts_http_client: HTTPClientConfig
    accounts_grpc_server: GRPCServerConfig
    accounts_grpc_client: GRPCClientConfig
    accounts_postgres_database: PostgresConfig

    documents_s3_client: S3ClientConfig
    documents_http_server: HTTPServerConfig
    documents_http_client: HTTPClientConfig
    documents_grpc_server: GRPCServerConfig
    documents_grpc_client: GRPCClientConfig

    operations_s3_client: S3ClientConfig
    operations_http_server: HTTPServerConfig
    operations_http_client: HTTPClientConfig
    operations_grpc_server: GRPCServerConfig
    operations_grpc_client: GRPCClientConfig
    operations_postgres_database: PostgresConfig


settings = Settings()
