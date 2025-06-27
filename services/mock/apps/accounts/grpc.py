from grpc.aio import ServicerContext

from contracts.services.accounts.accounts_service_pb2_grpc import AccountsServiceServicer
from contracts.services.accounts.rpc_create_account_pb2 import CreateAccountRequest, CreateAccountResponse
from contracts.services.accounts.rpc_get_account_pb2 import GetAccountRequest, GetAccountResponse
from contracts.services.accounts.rpc_get_accounts_pb2 import GetAccountsRequest, GetAccountsResponse
from contracts.services.accounts.rpc_update_account_balance_pb2 import (
    UpdateAccountBalanceRequest,
    UpdateAccountBalanceResponse
)
from services.mock.apps.accounts.mock import loader


class AccountsMockService(AccountsServiceServicer):
    async def GetAccount(self, request: GetAccountRequest, context: ServicerContext) -> GetAccountResponse:
        return await loader.load_grpc_with_timeout('GetAccount/default.json', GetAccountResponse)

    async def GetAccounts(self, request: GetAccountsRequest, context: ServicerContext) -> GetAccountsResponse:
        return await loader.load_grpc_with_timeout('GetAccounts/default.json', GetAccountsResponse)

    async def CreateAccount(self, request: CreateAccountRequest, context: ServicerContext) -> CreateAccountResponse:
        return await loader.load_grpc_with_timeout('CreateAccount/default.json', CreateAccountResponse)

    async def UpdateAccountBalance(
            self,
            request: UpdateAccountBalanceRequest,
            context: ServicerContext
    ) -> UpdateAccountBalanceResponse:
        return await loader.load_grpc_with_timeout(
            'UpdateAccountBalance/default.json', UpdateAccountBalanceResponse
        )
