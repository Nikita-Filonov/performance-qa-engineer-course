from grpc.aio import ServicerContext

from contracts.services.gateway.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.gateway.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceServicer
from services.gateway.apps.users.controllers.users.grpc import get_user, create_user
from services.users.clients.users.grpc import get_users_grpc_client


class UsersGatewayService(UsersGatewayServiceServicer):
    async def GetUser(self, request: GetUserRequest, context: ServicerContext) -> GetUserResponse:
        return await get_user(
            context=context,
            request=request,
            users_grpc_client=get_users_grpc_client()
        )

    async def CreateUser(
            self,
            request: CreateUserRequest,
            context: ServicerContext
    ) -> CreateUserResponse:
        return await create_user(
            context=context,
            request=request,
            users_grpc_client=get_users_grpc_client(),
        )
