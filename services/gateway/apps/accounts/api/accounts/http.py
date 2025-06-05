from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.accounts.clients.accounts.http import AccountsHTTPClient, get_accounts_http_client
from services.cards.clients.cards.http import CardsHTTPClient, get_cards_http_client
from services.documents.clients.contracts.http import ContractsHTTPClient, get_contracts_http_client
from services.documents.clients.tariffs.http import TariffsHTTPClient, get_tariffs_http_client
from services.gateway.apps.accounts.controllers.accounts.http import (
    get_accounts,
    open_deposit_account,
    open_savings_account,
    open_debit_card_account,
    open_credit_card_account
)
from services.gateway.apps.accounts.schema.accounts import (
    GetAccountsQuerySchema,
    GetAccountsResponseSchema,
    OpenSavingsAccountRequestSchema,
    OpenSavingsAccountResponseSchema,
    OpenDepositAccountRequestSchema,
    OpenDepositAccountResponseSchema,
    OpenDebitCardAccountRequestSchema,
    OpenDebitCardAccountResponseSchema,
    OpenCreditCardAccountRequestSchema,
    OpenCreditCardAccountResponseSchema
)
from services.users.clients.users.http import UsersHTTPClient, get_users_http_client

accounts_gateway_router = APIRouter(
    prefix=APIRoutes.ACCOUNTS,
    tags=[APIRoutes.ACCOUNTS.as_tag()]
)


@accounts_gateway_router.get('', response_model=GetAccountsResponseSchema)
async def get_accounts_view(
        query: Annotated[GetAccountsQuerySchema, Depends(GetAccountsQuerySchema.as_query)],
        cards_http_client: Annotated[CardsHTTPClient, Depends(get_cards_http_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)]
):
    return await get_accounts(
        query=query,
        cards_http_client=cards_http_client,
        accounts_http_client=accounts_http_client
    )


@accounts_gateway_router.post(
    '/open-deposit-account',
    response_model=OpenDepositAccountResponseSchema
)
async def open_deposit_account_view(
        request: OpenDepositAccountRequestSchema,
        tariffs_http_client: Annotated[TariffsHTTPClient, Depends(get_tariffs_http_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)],
        contracts_http_client: Annotated[ContractsHTTPClient, Depends(get_contracts_http_client)],
):
    return await open_deposit_account(
        request=request,
        tariffs_http_client=tariffs_http_client,
        accounts_http_client=accounts_http_client,
        contracts_http_client=contracts_http_client
    )


@accounts_gateway_router.post(
    '/open-savings-account',
    response_model=OpenSavingsAccountResponseSchema
)
async def open_savings_account_view(
        request: OpenSavingsAccountRequestSchema,
        tariffs_http_client: Annotated[TariffsHTTPClient, Depends(get_tariffs_http_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)],
        contracts_http_client: Annotated[ContractsHTTPClient, Depends(get_contracts_http_client)],
):
    return await open_savings_account(
        request=request,
        tariffs_http_client=tariffs_http_client,
        accounts_http_client=accounts_http_client,
        contracts_http_client=contracts_http_client
    )


@accounts_gateway_router.post(
    '/open-debit-card-account',
    response_model=OpenDebitCardAccountResponseSchema
)
async def open_debit_card_account_view(
        request: OpenDebitCardAccountRequestSchema,
        users_http_client: Annotated[UsersHTTPClient, Depends(get_users_http_client)],
        cards_http_client: Annotated[CardsHTTPClient, Depends(get_cards_http_client)],
        tariffs_http_client: Annotated[TariffsHTTPClient, Depends(get_tariffs_http_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)],
        contracts_http_client: Annotated[ContractsHTTPClient, Depends(get_contracts_http_client)],
):
    return await open_debit_card_account(
        request=request,
        users_http_client=users_http_client,
        cards_http_client=cards_http_client,
        tariffs_http_client=tariffs_http_client,
        accounts_http_client=accounts_http_client,
        contracts_http_client=contracts_http_client
    )


@accounts_gateway_router.post(
    '/open-credit-card-account',
    response_model=OpenCreditCardAccountResponseSchema
)
async def open_credit_card_account_view(
        request: OpenCreditCardAccountRequestSchema,
        users_http_client: Annotated[UsersHTTPClient, Depends(get_users_http_client)],
        cards_http_client: Annotated[CardsHTTPClient, Depends(get_cards_http_client)],
        tariffs_http_client: Annotated[TariffsHTTPClient, Depends(get_tariffs_http_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)],
        contracts_http_client: Annotated[ContractsHTTPClient, Depends(get_contracts_http_client)],
):
    return await open_credit_card_account(
        request=request,
        users_http_client=users_http_client,
        cards_http_client=cards_http_client,
        tariffs_http_client=tariffs_http_client,
        accounts_http_client=accounts_http_client,
        contracts_http_client=contracts_http_client
    )
