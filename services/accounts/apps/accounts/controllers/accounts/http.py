import uuid

from fastapi import HTTPException, status

from services.accounts.apps.accounts.schema.accounts import (
    AccountSchema,
    GetAccountsQuerySchema,
    GetAccountResponseSchema,
    GetAccountsResponseSchema,
    CreateAccountRequestSchema,
    CreateAccountResponseSchema,
    UpdateAccountBalanceRequestSchema,
    UpdateAccountBalanceResponseSchema
)
from services.accounts.services.postgres.repositories.accounts import (
    CreateAccountDict,
    UpdateAccountDict,
    AccountsRepository,
)
from services.users.clients.users.http import UsersHTTPClient, UsersHTTPClientError


async def get_account(
        account_id: uuid.UUID,
        accounts_repository: AccountsRepository
) -> GetAccountResponseSchema:
    account = await accounts_repository.get_by_id(account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with id {account_id} not found"
        )

    return GetAccountResponseSchema(account=AccountSchema.model_validate(account))


async def get_accounts(
        query: GetAccountsQuerySchema,
        accounts_repository: AccountsRepository
):
    accounts = await accounts_repository.filter(user_id=query.user_id)

    return GetAccountsResponseSchema(
        accounts=[AccountSchema.model_validate(account) for account in accounts]
    )


async def create_account(
        request: CreateAccountRequestSchema,
        users_http_client: UsersHTTPClient,
        accounts_repository: AccountsRepository
) -> CreateAccountResponseSchema:
    try:
        get_user_response = await users_http_client.get_user(request.user_id)
    except UsersHTTPClientError as error:
        raise HTTPException(
            detail=f"Create account: {error.details}",
            status_code=error.status_code
        )

    account = await accounts_repository.create(
        CreateAccountDict(
            type=request.type,
            status=request.status,
            user_id=get_user_response.user.id,
            balance=request.balance,
        )
    )

    return CreateAccountResponseSchema(account=AccountSchema.model_validate(account))


async def update_account_balance(
        request: UpdateAccountBalanceRequestSchema,
        accounts_repository: AccountsRepository
) -> UpdateAccountBalanceResponseSchema:
    account = await accounts_repository.update(
        request.account_id, UpdateAccountDict(balance=request.balance)
    )

    return UpdateAccountBalanceResponseSchema(account=AccountSchema.model_validate(account))
