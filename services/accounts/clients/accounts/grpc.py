from config import settings
from contracts.services.accounts.account_pb2 import Account, AccountType, AccountStatus
from contracts.services.accounts.accounts_service_pb2_grpc import AccountsServiceStub
from contracts.services.accounts.rpc_create_account_pb2 import CreateAccountRequest, CreateAccountResponse
from contracts.services.accounts.rpc_get_account_pb2 import GetAccountRequest, GetAccountResponse
from contracts.services.accounts.rpc_get_accounts_pb2 import GetAccountsRequest, GetAccountsResponse
from contracts.services.accounts.rpc_update_account_balance_pb2 import UpdateAccountBalanceRequest, \
    UpdateAccountBalanceResponse
from libs.grpc.client.base import GRPCClient
from libs.logger import get_logger


class AccountsGRPCClient(GRPCClient):
    stub: AccountsServiceStub
    stub_class = AccountsServiceStub

    async def get_account_api(self, request: GetAccountRequest) -> GetAccountResponse:
        return await self.stub.GetAccount(request)

    async def get_accounts_api(self, request: GetAccountsRequest) -> GetAccountsResponse:
        return await self.stub.GetAccounts(request)

    async def create_account_api(self, request: CreateAccountRequest) -> CreateAccountResponse:
        return await self.stub.CreateAccount(request)

    async def update_account_balance_api(self, request: UpdateAccountBalanceRequest) -> UpdateAccountBalanceResponse:
        return await self.stub.UpdateAccountBalance(request)

    async def get_account(self, account_id: str) -> Account:
        request = GetAccountRequest(id=account_id)
        response = await self.get_account_api(request)
        return response.account

    async def get_accounts(self, user_id: str) -> list[Account]:
        request = GetAccountsRequest(user_id=user_id)
        response = await self.get_accounts_api(request)
        return response.accounts

    async def update_account_balance(self, account_id: str, balance: float) -> Account:
        request = UpdateAccountBalanceRequest(account_id=account_id, balance=balance)
        response = await self.update_account_balance_api(request)
        return response.account

    async def create_deposit_account(self, user_id: str) -> Account:
        request = CreateAccountRequest(
            type=AccountType.ACCOUNT_TYPE_DEPOSIT,
            status=AccountStatus.ACCOUNT_STATUS_ACTIVE,
            user_id=user_id,
            balance=0
        )
        response = await self.create_account_api(request)
        return response.account

    async def create_savings_account(self, user_id: str) -> Account:
        request = CreateAccountRequest(
            type=AccountType.ACCOUNT_TYPE_SAVINGS,
            status=AccountStatus.ACCOUNT_STATUS_ACTIVE,
            user_id=user_id,
            balance=0
        )
        response = await self.create_account_api(request)
        return response.account

    async def create_debit_card_account(self, user_id: str) -> Account:
        request = CreateAccountRequest(
            type=AccountType.ACCOUNT_TYPE_DEBIT_CARD,
            status=AccountStatus.ACCOUNT_STATUS_ACTIVE,
            user_id=user_id,
            balance=0
        )
        response = await self.create_account_api(request)
        return response.account

    async def create_credit_card_account(self, user_id: str) -> Account:
        request = CreateAccountRequest(
            type=AccountType.ACCOUNT_TYPE_CREDIT_CARD,
            status=AccountStatus.ACCOUNT_STATUS_ACTIVE,
            user_id=user_id,
            balance=25000
        )
        response = await self.create_account_api(request)
        return response.account


def get_accounts_grpc_client() -> AccountsGRPCClient:
    logger = get_logger("ACCOUNTS_SERVICE_GRPC_CLIENT")
    return AccountsGRPCClient(config=settings.accounts_grpc_client, logger=logger)
