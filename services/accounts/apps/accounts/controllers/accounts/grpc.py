import uuid

from grpc import StatusCode
from grpc.aio import ServicerContext, AioRpcError

from contracts.services.accounts.account_pb2 import (
    Account,
    AccountType as ProtoAccountType,
    AccountStatus as ProtoAccountStatus
)
from contracts.services.accounts.rpc_create_account_pb2 import CreateAccountRequest, CreateAccountResponse
from contracts.services.accounts.rpc_get_account_pb2 import GetAccountRequest, GetAccountResponse
from contracts.services.accounts.rpc_get_accounts_pb2 import GetAccountsRequest, GetAccountsResponse
from contracts.services.accounts.rpc_update_account_balance_pb2 import (
    UpdateAccountBalanceRequest,
    UpdateAccountBalanceResponse
)
from services.accounts.services.postgres.models.accounts import AccountType, AccountStatus, AccountsModel
from services.accounts.services.postgres.repositories.accounts import (
    CreateAccountDict,
    UpdateAccountDict,
    AccountsRepository,
)
from services.users.clients.users.grpc import UsersGRPCClient

MAP_ACCOUNT_TYPE_TO_PROTO = AccountType.to_proto_map(ProtoAccountType)
MAP_ACCOUNT_TYPE_FROM_PROTO = AccountType.from_proto_map(ProtoAccountType)
MAP_ACCOUNT_STATUS_TO_PROTO = AccountStatus.to_proto_map(ProtoAccountStatus)
MAP_ACCOUNT_STATUS_FROM_PROTO = AccountStatus.from_proto_map(ProtoAccountStatus)


def build_account_from_model(model: AccountsModel) -> Account:
    return Account(
        id=str(model.id),
        type=MAP_ACCOUNT_TYPE_TO_PROTO[model.type],
        status=MAP_ACCOUNT_STATUS_TO_PROTO[model.status],
        user_id=str(model.user_id),
        balance=model.balance
    )


async def get_account(
        context: ServicerContext,
        request: GetAccountRequest,
        accounts_repository: AccountsRepository
) -> GetAccountResponse:
    account = await accounts_repository.get_by_id(uuid.UUID(request.id))
    if not account:
        await context.abort(
            code=StatusCode.NOT_FOUND,
            details=f"Account with id {request.id} not found"
        )

    return GetAccountResponse(account=build_account_from_model(account))


async def get_accounts(
        request: GetAccountsRequest,
        accounts_repository: AccountsRepository
) -> GetAccountsResponse:
    accounts = await accounts_repository.filter(user_id=uuid.UUID(request.user_id))

    return GetAccountsResponse(
        accounts=[build_account_from_model(account) for account in accounts]
    )


async def create_account(
        context: ServicerContext,
        request: CreateAccountRequest,
        users_grpc_client: UsersGRPCClient,
        accounts_repository: AccountsRepository
) -> CreateAccountResponse:
    try:
        user = await users_grpc_client.get_user(request.user_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Create account: {error.details()}"
        )

    account = await accounts_repository.create(
        CreateAccountDict(
            type=MAP_ACCOUNT_TYPE_FROM_PROTO[request.type],
            status=MAP_ACCOUNT_STATUS_FROM_PROTO[request.status],
            user_id=uuid.UUID(user.id),
            balance=request.balance,
        )
    )

    return CreateAccountResponse(account=build_account_from_model(account))


async def update_account_balance(
        request: UpdateAccountBalanceRequest,
        accounts_repository: AccountsRepository
) -> UpdateAccountBalanceResponse:
    account = await accounts_repository.update(
        uuid.UUID(request.account_id), UpdateAccountDict(balance=request.balance)
    )

    return UpdateAccountBalanceResponse(account=build_account_from_model(account))
