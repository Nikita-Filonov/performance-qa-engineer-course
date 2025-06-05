from concurrent import futures
from logging import Logger

import grpc

from libs.config.grpc import GRPCServerConfig
from libs.grpc.server.interceptors.exception_interceptor import GRPCExceptionInterceptor
from libs.grpc.server.interceptors.logger_interceptor import GRPCLoggerInterceptor


def build_grpc_server(config: GRPCServerConfig, logger: Logger) -> grpc.aio.Server:
    logger.info(f'Starting server at {config.url}')

    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=100),
        interceptors=[
            GRPCLoggerInterceptor(logger),
            GRPCExceptionInterceptor(logger)
        ]
    )
    server.add_insecure_port(config.url)

    return server
