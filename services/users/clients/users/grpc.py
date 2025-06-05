from config import settings
from contracts.services.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.users.user_pb2 import User
from contracts.services.users.users_service_pb2_grpc import UsersServiceStub
from libs.grpc.client.base import GRPCClient
from libs.logger import get_logger


class UsersGRPCClient(GRPCClient):
    stub: UsersServiceStub
    stub_class = UsersServiceStub

    async def get_user_api(self, request: GetUserRequest) -> GetUserResponse:
        return await self.stub.GetUser(request)

    async def create_user_api(self, request: CreateUserRequest) -> CreateUserResponse:
        return await self.stub.CreateUser(request)

    async def get_user(self, user_id: str) -> User:
        request = GetUserRequest(id=user_id)
        response = await self.get_user_api(request)
        return response.user

    async def create_user(
            self,
            email: str,
            last_name: str,
            first_name: str,
            middle_name: str,
            phone_number: str,
    ) -> User:
        request = CreateUserRequest(
            email=email,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            phone_number=phone_number
        )
        response = await self.create_user_api(request)
        return response.user


def get_users_grpc_client() -> UsersGRPCClient:
    logger = get_logger("USERS_SERVICE_GRPC_CLIENT")
    return UsersGRPCClient(config=settings.users_grpc_client, logger=logger)
