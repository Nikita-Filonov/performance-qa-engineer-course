import asyncio

from grpc.aio import AioRpcError, ServicerContext

from contracts.services.accounts.account_pb2 import Account
from contracts.services.cards.card_pb2 import Card
from contracts.services.gateway.accounts.account_pb2 import AccountView
from contracts.services.gateway.accounts.rpc_get_accounts_pb2 import GetAccountsRequest, GetAccountsResponse
from contracts.services.gateway.accounts.rpc_open_credit_card_account_pb2 import (
    OpenCreditCardAccountRequest,
    OpenCreditCardAccountResponse
)
from contracts.services.gateway.accounts.rpc_open_debit_card_account_pb2 import (
    OpenDebitCardAccountRequest,
    OpenDebitCardAccountResponse
)
from contracts.services.gateway.accounts.rpc_open_deposit_account_pb2 import (
    OpenDepositAccountRequest,
    OpenDepositAccountResponse
)
from contracts.services.gateway.accounts.rpc_open_savings_account_pb2 import (
    OpenSavingsAccountRequest,
    OpenSavingsAccountResponse
)
from libs.faker import fake
from services.accounts.clients.accounts.grpc import AccountsGRPCClient
from services.cards.clients.cards.grpc import CardsGRPCClient
from services.documents.services.kafka.producer import DocumentsKafkaProducerClient
from services.users.clients.users.grpc import UsersGRPCClient


def build_account_view(cards: tuple[Card, ...] | list[Card], account: Account) -> AccountView:
    return AccountView(
        id=account.id,
        type=account.type,
        cards=cards,
        status=account.status,
        balance=account.balance
    )


async def get_accounts(
        request: GetAccountsRequest,
        cards_grpc_client: CardsGRPCClient,
        accounts_grpc_client: AccountsGRPCClient
) -> GetAccountsResponse:
    accounts = await accounts_grpc_client.get_accounts(request.user_id)

    results: list[AccountView] = []
    for account in accounts:
        cards = await cards_grpc_client.get_cards(account.id)

        results.append(build_account_view(cards=cards, account=account))

    return GetAccountsResponse(accounts=results)


async def create_cards_for_account(
        context: ServicerContext,
        user_id: str,
        account_id: str,
        users_grpc_client: UsersGRPCClient,
        cards_grpc_client: CardsGRPCClient,
) -> tuple[Card, Card]:
    try:
        user = await users_grpc_client.get_user(user_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Open account: {error.details()}"
        )

    create_card_payload = dict(
        last_name=user.last_name,
        first_name=user.first_name,
        account_id=account_id
    )

    return await asyncio.gather(
        cards_grpc_client.create_virtual_card(**create_card_payload),
        cards_grpc_client.create_physical_card(**create_card_payload)
    )


async def create_documents_for_account(
        account_id: str,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
):
    await documents_kafka_producer_client.produce_tariff_document(
        account_id=account_id, content=fake.sentence().encode()
    )
    await documents_kafka_producer_client.produce_contract_document(
        account_id=account_id, content=fake.sentence().encode()
    )


async def open_deposit_account(
        request: OpenDepositAccountRequest,
        accounts_grpc_client: AccountsGRPCClient,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> OpenDepositAccountResponse:
    account = await accounts_grpc_client.create_deposit_account(request.user_id)

    await create_documents_for_account(account.id, documents_kafka_producer_client)

    return OpenDepositAccountResponse(account=build_account_view(cards=[], account=account))


async def open_savings_account(
        request: OpenSavingsAccountRequest,
        accounts_grpc_client: AccountsGRPCClient,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> OpenSavingsAccountResponse:
    account = await accounts_grpc_client.create_savings_account(request.user_id)

    await create_documents_for_account(account.id, documents_kafka_producer_client)

    return OpenSavingsAccountResponse(account=build_account_view(cards=[], account=account))


async def open_debit_card_account(
        context: ServicerContext,
        request: OpenDebitCardAccountRequest,
        users_grpc_client: UsersGRPCClient,
        cards_grpc_client: CardsGRPCClient,
        accounts_grpc_client: AccountsGRPCClient,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> OpenDebitCardAccountResponse:
    account = await accounts_grpc_client.create_debit_card_account(request.user_id)
    cards = await create_cards_for_account(
        context=context,
        user_id=request.user_id,
        account_id=account.id,
        users_grpc_client=users_grpc_client,
        cards_grpc_client=cards_grpc_client
    )

    await create_documents_for_account(account.id, documents_kafka_producer_client)

    return OpenDebitCardAccountResponse(account=build_account_view(cards=cards, account=account))


async def open_credit_card_account(
        context: ServicerContext,
        request: OpenCreditCardAccountRequest,
        users_grpc_client: UsersGRPCClient,
        cards_grpc_client: CardsGRPCClient,
        accounts_grpc_client: AccountsGRPCClient,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> OpenCreditCardAccountResponse:
    account = await accounts_grpc_client.create_credit_card_account(request.user_id)
    cards = await create_cards_for_account(
        context=context,
        user_id=request.user_id,
        account_id=account.id,
        users_grpc_client=users_grpc_client,
        cards_grpc_client=cards_grpc_client
    )

    await create_documents_for_account(account.id, documents_kafka_producer_client)

    return OpenCreditCardAccountResponse(account=build_account_view(cards=cards, account=account))
