import uuid

from grpc import StatusCode
from grpc.aio import ServicerContext

from contracts.services.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from contracts.services.users.user_pb2 import User
from services.users.services.postgres.models.users import UsersModel
from services.users.services.postgres.repositories.users import UsersRepository, CreateUserDict


def build_user_from_model(model: UsersModel) -> User:
    return User(
        id=str(model.id),
        email=model.email,
        last_name=model.last_name,
        first_name=model.first_name,
        middle_name=model.middle_name,
        phone_number=model.phone_number
    )


async def get_user(
        context: ServicerContext,
        request: GetUserRequest,
        users_repository: UsersRepository
) -> GetUserResponse:
    user = await users_repository.get_by_id(uuid.UUID(request.id))
    if not user:
        await context.abort(
            code=StatusCode.NOT_FOUND,
            details=f"User with id {request.id} not found"
        )

    return GetUserResponse(user=build_user_from_model(user))


async def create_user(
        context: ServicerContext,
        request: CreateUserRequest,
        users_repository: UsersRepository
) -> CreateUserResponse:
    user = await users_repository.get_by_email(request.email)
    if user:
        await context.abort(
            code=StatusCode.INVALID_ARGUMENT,
            details=f"User with email {request.email} already exists"
        )

    user = await users_repository.create(
        CreateUserDict(
            email=request.email,
            last_name=request.last_name,
            first_name=request.first_name,
            middle_name=request.middle_name,
            phone_number=request.phone_number
        )
    )

    return CreateUserResponse(user=build_user_from_model(user))
