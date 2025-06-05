from logging import Logger
from typing import Callable

import grpc
from grpc.aio import UnaryUnaryClientInterceptor, ClientCallDetails
from grpc.aio._call import UnaryUnaryCall
from grpc.aio._typing import RequestType, ResponseType


class GRPCRetriesInterceptor(UnaryUnaryClientInterceptor):
    def __init__(self, codes: list[grpc.StatusCode], retries: int, logger: Logger):
        self.codes = codes
        self.retries = retries
        self.logger = logger

    async def intercept_unary_unary(
            self,
            continuation: Callable[[ClientCallDetails, RequestType], UnaryUnaryCall],
            client_call_details: ClientCallDetails,
            request: RequestType,
    ) -> UnaryUnaryCall | ResponseType:
        response: UnaryUnaryCall = await continuation(client_call_details, request)
        if await response.code() not in self.codes:
            return response

        attempt = 0
        while attempt < self.retries:
            response = await continuation(client_call_details, request)
            code = await response.code()

            if code not in self.codes:
                return response

            self.logger.error(
                f'Unexpected response code: "{code}" for {client_call_details.method}, retrying'
            )

            attempt += 1

        return response
