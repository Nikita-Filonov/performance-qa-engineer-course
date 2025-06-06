import uuid

from grpc import StatusCode
from grpc.aio import AioRpcError, ServicerContext

from contracts.services.accounts.account_pb2 import AccountType
from contracts.services.cards.card_pb2 import (
    Card,
    CardType as ProtoCardType,
    CardStatus as ProtoCardStatus,
    CardPaymentSystem as ProtoCardPaymentSystem
)
from contracts.services.cards.rpc_create_card_pb2 import CreateCardRequest, CreateCardResponse
from contracts.services.cards.rpc_get_card_pb2 import GetCardRequest, GetCardResponse
from contracts.services.cards.rpc_get_cards_pb2 import GetCardsRequest, GetCardsResponse
from libs.base.date import to_proto_date, from_proto_date
from services.accounts.clients.accounts.grpc import AccountsGRPCClient
from services.cards.services.postgres.models.cards import (
    CardType,
    CardStatus,
    CardsModel,
    CardPaymentSystem
)
from services.cards.services.postgres.repositories.cards import CardsRepository, CreateCardDict

MAP_CARD_TYPE_TO_PROTO = CardType.to_proto_map(ProtoCardType)
MAP_CARD_TYPE_FROM_PROTO = CardType.from_proto_map(ProtoCardType)
MAP_CARD_STATUS_TO_PROTO = CardStatus.to_proto_map(ProtoCardStatus)
MAP_CARD_STATUS_FROM_PROTO = CardStatus.from_proto_map(ProtoCardStatus)
MAP_CARD_PAYMENT_SYSTEM_TO_PROTO = CardPaymentSystem.to_proto_map(ProtoCardPaymentSystem)
MAP_CARD_PAYMENT_SYSTEM_FROM_PROTO = CardPaymentSystem.from_proto_map(ProtoCardPaymentSystem)


def build_card_from_model(model: CardsModel) -> Card:
    return Card(
        id=str(model.id),
        pin=model.pin,
        cvv=model.cvv,
        type=MAP_CARD_TYPE_TO_PROTO[model.type],
        status=MAP_CARD_STATUS_TO_PROTO[model.status],
        account_id=str(model.account_id),
        card_number=model.card_number,
        card_holder=model.card_holder,
        expiry_date=to_proto_date(model.expiry_date),
        payment_system=MAP_CARD_PAYMENT_SYSTEM_TO_PROTO[model.payment_system]
    )


async def get_card(
        context: ServicerContext,
        request: GetCardRequest,
        cards_repository: CardsRepository
) -> GetCardResponse:
    card = await cards_repository.get_by_id(uuid.UUID(request.id))
    if not card:
        await context.abort(
            code=StatusCode.NOT_FOUND,
            details=f"Card with id {request.id} not found"
        )

    return GetCardResponse(card=build_card_from_model(card))


async def get_cards(
        request: GetCardsRequest,
        cards_repository: CardsRepository
) -> GetCardsResponse:
    cards = await cards_repository.filter(account_id=uuid.UUID(request.account_id))

    return GetCardsResponse(cards=[build_card_from_model(card) for card in cards])


async def create_card(
        context: ServicerContext,
        request: CreateCardRequest,
        cards_repository: CardsRepository,
        accounts_grpc_client: AccountsGRPCClient,
) -> CreateCardResponse:
    try:
        account = await accounts_grpc_client.get_account(request.account_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Create card: {error.details()}"
        )

    supported_accounts = [AccountType.ACCOUNT_TYPE_DEBIT_CARD, AccountType.ACCOUNT_TYPE_CREDIT_CARD]
    if account.type not in supported_accounts:
        await context.abort(
            code=StatusCode.FAILED_PRECONDITION,
            details=f"Create card: unsupported account type {account.type}"
        )

    card = await cards_repository.create(
        CreateCardDict(
            pin=request.pin,
            cvv=request.cvv,
            type=MAP_CARD_TYPE_FROM_PROTO[request.type],
            status=MAP_CARD_STATUS_FROM_PROTO[request.status],
            account_id=uuid.UUID(account.id),
            card_number=request.card_number,
            card_holder=request.card_holder,
            expiry_date=from_proto_date(request.expiry_date),
            payment_system=MAP_CARD_PAYMENT_SYSTEM_FROM_PROTO[request.payment_system]
        )
    )

    return CreateCardResponse(card=build_card_from_model(card))
