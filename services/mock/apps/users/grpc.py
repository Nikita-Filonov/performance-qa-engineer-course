from grpc.aio import ServicerContext

from contracts.services.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.users.users_service_pb2_grpc import UsersServiceServicer
from services.mock.apps.users.mock import loader


class UsersMockService(UsersServiceServicer):
    async def GetUser(self, request: GetUserRequest, context: ServicerContext) -> GetUserResponse:
        return loader.load_grpc("GetUser/default.json", GetUserResponse)

    async def CreateUser(self, request: CreateUserRequest, context: ServicerContext) -> CreateUserResponse:
        return loader.load_grpc("CreateUser/default.json", CreateUserResponse)
