from config import settings
from contracts.services.cards.card_pb2 import Card, CardType, CardStatus, CardPaymentSystem
from contracts.services.cards.cards_service_pb2_grpc import CardsServiceStub
from contracts.services.cards.rpc_create_card_pb2 import CreateCardRequest, CreateCardResponse
from contracts.services.cards.rpc_get_card_pb2 import GetCardRequest, GetCardResponse
from contracts.services.cards.rpc_get_cards_pb2 import GetCardsRequest, GetCardsResponse
from libs.base.date import to_proto_date
from libs.faker import fake
from libs.grpc.client.base import GRPCClient
from libs.logger import get_logger
from services.cards.clients.cards.base import build_card_expired_at, build_card_holder


class CardsGRPCClient(GRPCClient):
    stub: CardsServiceStub
    stub_class = CardsServiceStub

    async def get_card_api(self, request: GetCardRequest) -> GetCardResponse:
        return await self.stub.GetCard(request)

    async def get_cards_api(self, request: GetCardsRequest) -> GetCardsResponse:
        return await self.stub.GetCards(request)

    async def create_card_api(self, request: CreateCardRequest) -> CreateCardResponse:
        return await self.stub.CreateCard(request)

    async def get_card(self, card_id: str) -> Card:
        request = GetCardRequest(id=card_id)
        response = await self.get_card_api(request)
        return response.card

    async def get_cards(self, account_id: str) -> list[Card]:
        request = GetCardsRequest(account_id=account_id)
        response = await self.get_cards_api(request)
        return response.cards

    async def create_virtual_card(self, first_name: str, last_name: str, account_id: str) -> Card:
        request = CreateCardRequest(
            pin=fake.card_pin(),
            cvv=fake.card_cvv(),
            type=CardType.CARD_TYPE_VIRTUAL,
            status=CardStatus.CARD_STATUS_ACTIVE,
            account_id=account_id,
            card_number=fake.card_number(),
            card_holder=build_card_holder(first_name=first_name, last_name=last_name),
            expiry_date=to_proto_date(build_card_expired_at()),
            payment_system=CardPaymentSystem.CARD_PAYMENT_SYSTEM_MASTERCARD
        )
        response = await self.create_card_api(request)
        return response.card

    async def create_physical_card(self, first_name: str, last_name: str, account_id: str) -> Card:
        request = CreateCardRequest(
            pin=fake.card_pin(),
            cvv=fake.card_cvv(),
            type=CardType.CARD_TYPE_PHYSICAL,
            status=CardStatus.CARD_STATUS_ACTIVE,
            account_id=account_id,
            card_number=fake.card_number(),
            card_holder=build_card_holder(first_name=first_name, last_name=last_name),
            expiry_date=to_proto_date(build_card_expired_at()),
            payment_system=CardPaymentSystem.CARD_PAYMENT_SYSTEM_MASTERCARD
        )
        response = await self.create_card_api(request)
        return response.card


def get_cards_grpc_client() -> CardsGRPCClient:
    logger = get_logger("CARDS_SERVICE_GRPC_CLIENT")
    return CardsGRPCClient(config=settings.cards_grpc_client, logger=logger)
