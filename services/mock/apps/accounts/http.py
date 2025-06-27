import uuid

from fastapi import APIRouter

from libs.routes import APIRoutes
from services.accounts.apps.accounts.schema.accounts import (
    GetAccountResponseSchema,
    GetAccountsResponseSchema,
    CreateAccountRequestSchema,
    CreateAccountResponseSchema,
    UpdateAccountBalanceRequestSchema,
    UpdateAccountBalanceResponseSchema
)
from services.mock.apps.accounts.mock import loader

accounts_mock_router = APIRouter(
    prefix=APIRoutes.ACCOUNTS,
    tags=[APIRoutes.ACCOUNTS.as_tag()]
)


@accounts_mock_router.get('', response_model=GetAccountsResponseSchema)
async def get_accounts_view():
    return await loader.load_http_with_timeout("get_accounts/default.json", GetAccountsResponseSchema)


@accounts_mock_router.get('/{account_id}', response_model=GetAccountResponseSchema)
async def get_account_view(account_id: uuid.UUID):
    return await loader.load_http_with_timeout("get_account/default.json", GetAccountResponseSchema)


@accounts_mock_router.post('', response_model=CreateAccountResponseSchema)
async def create_account_view(request: CreateAccountRequestSchema):
    return await loader.load_http_with_timeout("create_account/default.json", CreateAccountResponseSchema)


@accounts_mock_router.post(
    '/update-account-balance',
    response_model=UpdateAccountBalanceResponseSchema
)
async def update_account_balance_view(request: UpdateAccountBalanceRequestSchema):
    return await loader.load_http_with_timeout(
        "update_account_balance/default.json", UpdateAccountBalanceResponseSchema
    )
