from grpc.aio import ServicerContext

from contracts.services.cards.cards_service_pb2_grpc import CardsServiceServicer
from contracts.services.cards.rpc_create_card_pb2 import CreateCardRequest, CreateCardResponse
from contracts.services.cards.rpc_get_card_pb2 import GetCardRequest, GetCardResponse
from contracts.services.cards.rpc_get_cards_pb2 import GetCardsRequest, GetCardsResponse
from services.accounts.clients.accounts.grpc import get_accounts_grpc_client
from services.cards.apps.cards.controllers.cards.grpc import create_card, get_card, get_cards
from services.cards.services.postgres.repositories.cards import get_cards_repository_context


class CardsService(CardsServiceServicer):
    async def GetCard(self, request: GetCardRequest, context: ServicerContext) -> GetCardResponse:
        async with get_cards_repository_context() as cards_repository:
            return await get_card(context, request, cards_repository)

    async def GetCards(self, request: GetCardsRequest, context: ServicerContext) -> GetCardsResponse:
        async with get_cards_repository_context() as cards_repository:
            return await get_cards(request, cards_repository)

    async def CreateCard(self, request: CreateCardRequest, context: ServicerContext) -> CreateCardResponse:
        async with get_cards_repository_context() as cards_repository:
            return await create_card(
                context=context,
                request=request,
                cards_repository=cards_repository,
                accounts_grpc_client=get_accounts_grpc_client()
            )
