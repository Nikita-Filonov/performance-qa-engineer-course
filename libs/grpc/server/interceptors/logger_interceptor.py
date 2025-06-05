from logging import Logger
from typing import Callable, Awaitable

from grpc import RpcMethodHandler, HandlerCallDetails
from grpc.aio import ServerInterceptor


class GRPCLoggerInterceptor(ServerInterceptor):
    def __init__(self, logger: Logger):
        self.logger = logger

    async def intercept_service(
            self,
            continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
            handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        handler = await continuation(handler_call_details)

        if hasattr(handler, 'unary_unary'):
            original_handler = handler.unary_unary

            async def new_unary_unary(request, context):
                self.logger.info(f"Request: {handler_call_details.method}")
                response = await original_handler(request, context)
                self.logger.info(f"Response: {handler_call_details.method}")
                return response

            return handler._replace(unary_unary=new_unary_unary)

        return handler
