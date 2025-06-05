from grpc.aio import ServicerContext

from contracts.services.accounts.accounts_service_pb2_grpc import AccountsServiceServicer
from contracts.services.accounts.rpc_create_account_pb2 import CreateAccountRequest, CreateAccountResponse
from contracts.services.accounts.rpc_get_account_pb2 import GetAccountRequest, GetAccountResponse
from contracts.services.accounts.rpc_get_accounts_pb2 import GetAccountsRequest, GetAccountsResponse
from contracts.services.accounts.rpc_update_account_balance_pb2 import (
    UpdateAccountBalanceRequest,
    UpdateAccountBalanceResponse
)
from services.accounts.apps.accounts.controllers.accounts.grpc import create_account, get_accounts, get_account, \
    update_account_balance
from services.accounts.services.postgres.repositories.accounts import get_accounts_repository_context
from services.users.clients.users.grpc import get_users_grpc_client


class AccountsService(AccountsServiceServicer):
    async def GetAccount(self, request: GetAccountRequest, context: ServicerContext) -> GetAccountResponse:
        async with get_accounts_repository_context() as accounts_repository:
            return await get_account(context, request, accounts_repository)

    async def GetAccounts(self, request: GetAccountsRequest, context: ServicerContext) -> GetAccountsResponse:
        async with get_accounts_repository_context() as accounts_repository:
            return await get_accounts(request, accounts_repository)

    async def CreateAccount(self, request: CreateAccountRequest, context: ServicerContext) -> CreateAccountResponse:
        async with get_accounts_repository_context() as accounts_repository:
            return await create_account(
                context=context,
                request=request,
                users_grpc_client=get_users_grpc_client(),
                accounts_repository=accounts_repository
            )

    async def UpdateAccountBalance(
            self,
            request: UpdateAccountBalanceRequest,
            context: ServicerContext
    ) -> UpdateAccountBalanceResponse:
        async with get_accounts_repository_context() as accounts_repository:
            return await update_account_balance(request, accounts_repository)
