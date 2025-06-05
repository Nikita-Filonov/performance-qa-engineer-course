from abc import ABC, abstractmethod
from logging import Logger
from typing import Type

import grpc
import grpc.experimental.gevent as grpc_gevent

from libs.config.grpc import GRPCClientConfig
from libs.grpc.client.interceptors.logger_interceptor import GRPCLoggerInterceptor
from libs.grpc.client.interceptors.retries_interceptor import GRPCRetriesInterceptor
from libs.grpc.client.interceptors.timeout_interceptor import GRPCTimeoutInterceptor

grpc_gevent.init_gevent()


class GRPCStub(ABC):
    @abstractmethod
    def __init__(self, channel: grpc.Channel):
        pass


class GRPCClient:
    stub: GRPCStub
    stub_class: Type[GRPCStub]
    retry_codes: list[grpc.StatusCode] = [
        grpc.StatusCode.INTERNAL,
        grpc.StatusCode.UNAVAILABLE,
        grpc.StatusCode.DEADLINE_EXCEEDED,
        grpc.StatusCode.RESOURCE_EXHAUSTED,
    ]

    def __init__(self, config: GRPCClientConfig, logger: Logger):
        interceptors = [
            GRPCLoggerInterceptor(logger=logger),
            GRPCTimeoutInterceptor(timeout=config.timeout),
            GRPCRetriesInterceptor(codes=self.retry_codes, retries=config.retries, logger=logger)
        ]

        self.channel = grpc.aio.insecure_channel(config.url, interceptors=interceptors)
        self.stub = self.stub_class(self.channel)
