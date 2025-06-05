import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.accounts.clients.accounts.http import AccountsHTTPClient, get_accounts_http_client
from services.cards.apps.cards.controllers.cards.http import get_cards, get_card, create_card
from services.cards.apps.cards.schema.cards import (
    GetCardResponseSchema,
    GetCardsQuerySchema,
    GetCardsResponseSchema,
    CreateCardRequestSchema,
    CreateCardResponseSchema
)
from services.cards.services.postgres.repositories.cards import CardsRepository, get_cards_repository_depends

cards_router = APIRouter(
    prefix=APIRoutes.CARDS,
    tags=[APIRoutes.CARDS.as_tag()]
)


@cards_router.get('', response_model=GetCardsResponseSchema)
async def get_cards_view(
        query: Annotated[GetCardsQuerySchema, Depends(GetCardsQuerySchema.as_query)],
        cards_repository: Annotated[CardsRepository, Depends(get_cards_repository_depends)]
):
    return await get_cards(query, cards_repository)


@cards_router.get('/{card_id}', response_model=GetCardResponseSchema)
async def get_card_view(
        card_id: uuid.UUID,
        cards_repository: Annotated[CardsRepository, Depends(get_cards_repository_depends)]
):
    return await get_card(card_id, cards_repository)


@cards_router.post('', response_model=CreateCardResponseSchema)
async def create_card_view(
        request: CreateCardRequestSchema,
        cards_repository: Annotated[CardsRepository, Depends(get_cards_repository_depends)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)],
):
    return await create_card(
        request=request,
        cards_repository=cards_repository,
        accounts_http_client=accounts_http_client
    )
