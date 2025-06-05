import uuid

from httpx import Response, QueryParams

from config import settings
from libs.http.client.base import HTTPClient
from libs.http.client.handlers import handle_http_error, HTTPClientError
from libs.logger import get_logger
from libs.routes import APIRoutes
from services.accounts.apps.accounts.schema.accounts import (
    GetAccountResponseSchema,
    GetAccountsQuerySchema,
    GetAccountsResponseSchema,
    CreateAccountRequestSchema,
    CreateAccountResponseSchema,
    UpdateAccountBalanceRequestSchema,
    UpdateAccountBalanceResponseSchema
)
from services.accounts.services.postgres.models.accounts import AccountType, AccountStatus


class AccountsHTTPClientError(HTTPClientError):
    pass


class AccountsHTTPClient(HTTPClient):
    @handle_http_error(client='AccountsHTTPClient', exception=AccountsHTTPClientError)
    async def get_account_api(self, account_id: uuid.UUID) -> Response:
        return await self.get(f'{APIRoutes.ACCOUNTS}/{account_id}')

    @handle_http_error(client='AccountsHTTPClient', exception=AccountsHTTPClientError)
    async def get_accounts_api(self, query: GetAccountsQuerySchema) -> Response:
        return await self.get(
            APIRoutes.ACCOUNTS,
            params=QueryParams(**query.model_dump(mode='json', by_alias=True))
        )

    @handle_http_error(client='AccountsHTTPClient', exception=AccountsHTTPClientError)
    async def create_account_api(self, request: CreateAccountRequestSchema) -> Response:
        return await self.post(
            APIRoutes.ACCOUNTS, json=request.model_dump(mode='json', by_alias=True)
        )

    @handle_http_error(client='AccountsHTTPClient', exception=AccountsHTTPClientError)
    async def update_account_balance_api(self, request: UpdateAccountBalanceRequestSchema) -> Response:
        return await self.post(
            f'{APIRoutes.ACCOUNTS}/update-account-balance',
            json=request.model_dump(mode='json', by_alias=True)
        )

    async def get_account(self, account_id: uuid.UUID) -> GetAccountResponseSchema:
        response = await self.get_account_api(account_id)
        return GetAccountResponseSchema.model_validate_json(response.text)

    async def get_accounts(self, user_id: uuid.UUID) -> GetAccountsResponseSchema:
        query = GetAccountsQuerySchema(user_id=user_id)
        response = await self.get_accounts_api(query)
        return GetAccountsResponseSchema.model_validate_json(response.text)

    async def update_account_balance(
            self,
            account_id: uuid.UUID,
            balance: float
    ) -> UpdateAccountBalanceResponseSchema:
        request = UpdateAccountBalanceRequestSchema(account_id=account_id, balance=balance)
        response = await self.update_account_balance_api(request)
        return UpdateAccountBalanceResponseSchema.model_validate_json(response.text)

    async def create_deposit_account(self, user_id: uuid.UUID) -> CreateAccountResponseSchema:
        request = CreateAccountRequestSchema(
            type=AccountType.DEPOSIT,
            status=AccountStatus.ACTIVE,
            user_id=user_id,
            balance=0
        )
        response = await self.create_account_api(request)
        return CreateAccountResponseSchema.model_validate_json(response.text)

    async def create_savings_account(self, user_id: uuid.UUID) -> CreateAccountResponseSchema:
        request = CreateAccountRequestSchema(
            type=AccountType.SAVINGS,
            status=AccountStatus.ACTIVE,
            user_id=user_id,
            balance=0
        )
        response = await self.create_account_api(request)
        return CreateAccountResponseSchema.model_validate_json(response.text)

    async def create_debit_card_account(self, user_id: uuid.UUID) -> CreateAccountResponseSchema:
        request = CreateAccountRequestSchema(
            type=AccountType.DEBIT_CARD,
            status=AccountStatus.ACTIVE,
            user_id=user_id,
            balance=0
        )
        response = await self.create_account_api(request)
        return CreateAccountResponseSchema.model_validate_json(response.text)

    async def create_credit_card_account(self, user_id: uuid.UUID) -> CreateAccountResponseSchema:
        request = CreateAccountRequestSchema(
            type=AccountType.CREDIT_CARD,
            status=AccountStatus.ACTIVE,
            user_id=user_id,
            balance=25000
        )
        response = await self.create_account_api(request)
        return CreateAccountResponseSchema.model_validate_json(response.text)


def get_accounts_http_client() -> AccountsHTTPClient:
    logger = get_logger("ACCOUNTS_SERVICE_HTTP_CLIENT")
    return AccountsHTTPClient(config=settings.accounts_http_client, logger=logger)
