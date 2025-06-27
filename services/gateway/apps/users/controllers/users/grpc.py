from email_validator import validate_email
from email_validator.exceptions_types import EmailSyntaxError, EmailNotValidError
from grpc import StatusCode
from grpc.aio import ServicerContext, AioRpcError

from contracts.services.users.rpc_create_user_pb2 import CreateUserRequest, CreateUserResponse
from contracts.services.users.rpc_get_user_pb2 import GetUserRequest, GetUserResponse
from services.users.clients.users.grpc import UsersGRPCClient


async def get_user(
        context: ServicerContext,
        request: GetUserRequest,
        users_grpc_client: UsersGRPCClient
) -> GetUserResponse:
    try:
        user = await users_grpc_client.get_user(request.id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Get user: {error.details()}"
        )

    return GetUserResponse(user=user)


async def create_user(
        context: ServicerContext,
        request: CreateUserRequest,
        users_grpc_client: UsersGRPCClient
) -> CreateUserResponse:
    try:
        email = validate_email(request.email, test_environment=True)
    except (EmailSyntaxError, EmailNotValidError) as error:
        await context.abort(
            code=StatusCode.INVALID_ARGUMENT,
            details=f"Create user: {error}"
        )

    try:
        user = await users_grpc_client.create_user(
            email=email.original,
            last_name=request.last_name,
            first_name=request.first_name,
            middle_name=request.middle_name,
            phone_number=request.phone_number
        )
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Create user: {error}"
        )

    return CreateUserResponse(user=user)
