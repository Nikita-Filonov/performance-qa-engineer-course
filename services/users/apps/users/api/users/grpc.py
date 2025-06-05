from grpc.aio import ServicerContext

from contracts.services.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.users.users_service_pb2_grpc import UsersServiceServicer
from services.users.apps.users.controllers.users.grpc import create_user, get_user
from services.users.services.postgres.repositories.users import get_users_repository_context


class UsersService(UsersServiceServicer):
    async def GetUser(self, request: GetUserRequest, context: ServicerContext) -> GetUserResponse:
        async with get_users_repository_context() as users_repository:
            return await get_user(context, request, users_repository)

    async def CreateUser(self, request: CreateUserRequest, context: ServicerContext) -> CreateUserResponse:
        async with get_users_repository_context() as users_repository:
            return await create_user(context, request, users_repository)
