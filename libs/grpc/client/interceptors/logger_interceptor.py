from logging import Logger
from typing import Callable

from grpc.aio import UnaryUnaryClientInterceptor, ClientCallDetails
from grpc.aio._call import UnaryUnaryCall
from grpc.aio._typing import RequestType, ResponseType


class GRPCLoggerInterceptor(UnaryUnaryClientInterceptor):
    def __init__(self, logger: Logger):
        self.logger = logger

    async def intercept_unary_unary(
            self,
            continuation: Callable[[ClientCallDetails, RequestType], UnaryUnaryCall],
            client_call_details: ClientCallDetails,
            request: RequestType,
    ) -> UnaryUnaryCall | ResponseType:
        self.logger.info(f"REQUEST: {client_call_details.method}")

        response = await continuation(client_call_details, request)

        self.logger.info(f"RESPONSE: {client_call_details.method}")

        return response
