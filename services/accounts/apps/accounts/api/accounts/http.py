import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.accounts.apps.accounts.controllers.accounts.http import (
    get_account,
    get_accounts,
    create_account,
    update_account_balance
)
from services.accounts.apps.accounts.schema.accounts import (
    GetAccountResponseSchema,
    GetAccountsQuerySchema,
    GetAccountsResponseSchema,
    CreateAccountRequestSchema,
    CreateAccountResponseSchema,
    UpdateAccountBalanceRequestSchema,
    UpdateAccountBalanceResponseSchema
)
from services.accounts.services.postgres.repositories.accounts import AccountsRepository, \
    get_accounts_repository_depends
from services.users.clients.users.http import UsersHTTPClient, get_users_http_client

accounts_router = APIRouter(
    prefix=APIRoutes.ACCOUNTS,
    tags=[APIRoutes.ACCOUNTS.as_tag()]
)


@accounts_router.get('', response_model=GetAccountsResponseSchema)
async def get_accounts_view(
        query: Annotated[GetAccountsQuerySchema, Depends(GetAccountsQuerySchema.as_query)],
        accounts_repository: Annotated[AccountsRepository, Depends(get_accounts_repository_depends)]
):
    return await get_accounts(query, accounts_repository)


@accounts_router.get('/{account_id}', response_model=GetAccountResponseSchema)
async def get_account_view(
        account_id: uuid.UUID,
        accounts_repository: Annotated[AccountsRepository, Depends(get_accounts_repository_depends)]
):
    return await get_account(account_id, accounts_repository)


@accounts_router.post('', response_model=CreateAccountResponseSchema)
async def create_account_view(
        request: CreateAccountRequestSchema,
        users_http_client: Annotated[UsersHTTPClient, Depends(get_users_http_client)],
        accounts_repository: Annotated[AccountsRepository, Depends(get_accounts_repository_depends)]
):
    return await create_account(
        request=request,
        users_http_client=users_http_client,
        accounts_repository=accounts_repository
    )


@accounts_router.post(
    '/update-account-balance',
    response_model=UpdateAccountBalanceResponseSchema
)
async def update_account_balance_view(
        request: UpdateAccountBalanceRequestSchema,
        accounts_repository: Annotated[AccountsRepository, Depends(get_accounts_repository_depends)]
):
    return await update_account_balance(request, accounts_repository)
