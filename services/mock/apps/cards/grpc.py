from grpc.aio import ServicerContext

from contracts.services.cards.cards_service_pb2_grpc import CardsServiceServicer
from contracts.services.cards.rpc_create_card_pb2 import CreateCardRequest, CreateCardResponse
from contracts.services.cards.rpc_get_card_pb2 import GetCardRequest, GetCardResponse
from contracts.services.cards.rpc_get_cards_pb2 import GetCardsRequest, GetCardsResponse
from services.mock.apps.cards.mock import loader


class CardsMockService(CardsServiceServicer):
    async def GetCard(self, request: GetCardRequest, context: ServicerContext) -> GetCardResponse:
        return await loader.load_grpc_with_timeout("GetCard/default.json", GetCardResponse)

    async def GetCards(self, request: GetCardsRequest, context: ServicerContext) -> GetCardsResponse:
        return await loader.load_grpc_with_timeout("GetCards/default.json", GetCardsResponse)

    async def CreateCard(self, request: CreateCardRequest, context: ServicerContext) -> CreateCardResponse:
        return await loader.load_grpc_with_timeout("CreateCard/default.json", CreateCardResponse)
