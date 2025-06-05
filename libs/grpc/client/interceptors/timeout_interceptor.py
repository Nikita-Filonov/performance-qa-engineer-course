from typing import Callable

from grpc.aio import UnaryUnaryClientInterceptor, ClientCallDetails
from grpc.aio._call import UnaryUnaryCall
from grpc.aio._typing import RequestType, ResponseType


class GRPCTimeoutInterceptor(UnaryUnaryClientInterceptor):
    def __init__(self, timeout: float):
        self.timeout = timeout

    async def intercept_unary_unary(
            self,
            continuation: Callable[[ClientCallDetails, RequestType], UnaryUnaryCall],
            client_call_details: ClientCallDetails,
            request: RequestType,
    ) -> UnaryUnaryCall | ResponseType:
        if client_call_details.timeout is None:
            client_call_details = client_call_details._replace(timeout=self.timeout)

        return await continuation(client_call_details, request)
