from logging import Logger
from typing import Callable, Awaitable

from grpc import RpcMethodHandler, HandlerCallDetails
from grpc.aio import ServerInterceptor, ServicerContext, AioRpcError


class GRPCExceptionInterceptor(ServerInterceptor):
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

            async def new_unary_unary(request, context: ServicerContext):
                try:
                    response = await original_handler(request, context)
                except AioRpcError as error:
                    self.logger.error(f"Exception. Code: {error.code()}. Details: {error.details()}")
                    await context.abort(code=error.code(), details=error.details())

                return response

            return handler._replace(unary_unary=new_unary_unary)

        return handler
