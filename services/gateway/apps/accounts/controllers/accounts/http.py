import uuid

from fastapi import HTTPException

from libs.faker import fake
from services.accounts.apps.accounts.schema.accounts import AccountSchema
from services.accounts.clients.accounts.http import AccountsHTTPClient
from services.cards.apps.cards.schema.cards import CardSchema
from services.cards.clients.cards.http import CardsHTTPClient
from services.documents.services.kafka.producer import DocumentsKafkaProducerClient
from services.gateway.apps.accounts.schema.accounts import (
    AccountViewSchema,
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
from services.users.clients.users.http import UsersHTTPClient, UsersHTTPClientError


def build_account_view(cards: list[CardSchema], account: AccountSchema) -> AccountViewSchema:
    return AccountViewSchema(
        id=account.id,
        type=account.type,
        cards=cards,
        status=account.status,
        balance=account.balance
    )


async def get_accounts(
        query: GetAccountsQuerySchema,
        cards_http_client: CardsHTTPClient,
        accounts_http_client: AccountsHTTPClient
) -> GetAccountsResponseSchema:
    get_accounts_response = await accounts_http_client.get_accounts(user_id=query.user_id)

    results: list[AccountViewSchema] = []
    for account in get_accounts_response.accounts:
        get_cards_response = await cards_http_client.get_cards(account.id)

        results.append(build_account_view(cards=get_cards_response.cards, account=account))

    return GetAccountsResponseSchema(accounts=results)


async def create_cards_for_account(
        user_id: uuid.UUID,
        account_id: uuid.UUID,
        users_http_client: UsersHTTPClient,
        cards_http_client: CardsHTTPClient,
) -> list[CardSchema]:
    try:
        get_user_response = await users_http_client.get_user(user_id)
    except UsersHTTPClientError as error:
        raise HTTPException(
            detail=f"Open account: {error.details}",
            status_code=error.status_code
        )

    create_virtual_card_response = await cards_http_client.create_virtual_card(
        last_name=get_user_response.user.last_name,
        first_name=get_user_response.user.first_name,
        account_id=account_id
    )
    create_physical_card_response = await cards_http_client.create_physical_card(
        last_name=get_user_response.user.last_name,
        first_name=get_user_response.user.first_name,
        account_id=account_id
    )

    return [create_virtual_card_response.card, create_physical_card_response.card]


async def create_documents_for_account(
        account_id: uuid.UUID,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
):
    await documents_kafka_producer_client.produce_tariff_document(
        account_id=str(account_id), content=fake.sentence().encode()
    )
    await documents_kafka_producer_client.produce_contract_document(
        account_id=str(account_id), content=fake.sentence().encode()
    )


async def open_deposit_account(
        request: OpenDepositAccountRequestSchema,
        accounts_http_client: AccountsHTTPClient,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> OpenDepositAccountResponseSchema:
    create_account_response = await accounts_http_client.create_deposit_account(request.user_id)

    await create_documents_for_account(
        account_id=create_account_response.account.id,
        documents_kafka_producer_client=documents_kafka_producer_client
    )

    return OpenDepositAccountResponseSchema(
        account=build_account_view(cards=[], account=create_account_response.account)
    )


async def open_savings_account(
        request: OpenSavingsAccountRequestSchema,
        accounts_http_client: AccountsHTTPClient,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> OpenSavingsAccountResponseSchema:
    create_account_response = await accounts_http_client.create_savings_account(request.user_id)

    await create_documents_for_account(
        account_id=create_account_response.account.id,
        documents_kafka_producer_client=documents_kafka_producer_client
    )

    return OpenSavingsAccountResponseSchema(
        account=build_account_view(cards=[], account=create_account_response.account)
    )


async def open_debit_card_account(
        request: OpenDebitCardAccountRequestSchema,
        users_http_client: UsersHTTPClient,
        cards_http_client: CardsHTTPClient,
        accounts_http_client: AccountsHTTPClient,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> OpenDebitCardAccountResponseSchema:
    create_account_response = await accounts_http_client.create_debit_card_account(request.user_id)
    cards = await create_cards_for_account(
        user_id=request.user_id,
        account_id=create_account_response.account.id,
        users_http_client=users_http_client,
        cards_http_client=cards_http_client
    )

    await create_documents_for_account(
        account_id=create_account_response.account.id,
        documents_kafka_producer_client=documents_kafka_producer_client
    )

    return OpenDebitCardAccountResponseSchema(
        account=build_account_view(cards=cards, account=create_account_response.account)
    )


async def open_credit_card_account(
        request: OpenCreditCardAccountRequestSchema,
        users_http_client: UsersHTTPClient,
        cards_http_client: CardsHTTPClient,
        accounts_http_client: AccountsHTTPClient,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> OpenCreditCardAccountResponseSchema:
    create_account_response = await accounts_http_client.create_credit_card_account(request.user_id)
    cards = await create_cards_for_account(
        user_id=request.user_id,
        account_id=create_account_response.account.id,
        users_http_client=users_http_client,
        cards_http_client=cards_http_client
    )

    await create_documents_for_account(
        account_id=create_account_response.account.id,
        documents_kafka_producer_client=documents_kafka_producer_client,
    )

    return OpenCreditCardAccountResponseSchema(
        account=build_account_view(cards=cards, account=create_account_response.account)
    )
