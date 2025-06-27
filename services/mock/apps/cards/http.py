import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.cards.apps.cards.schema.cards import (
    GetCardResponseSchema,
    GetCardsQuerySchema,
    GetCardsResponseSchema,
    CreateCardRequestSchema,
    CreateCardResponseSchema
)
from services.mock.apps.cards.mock import loader

cards_mock_router = APIRouter(
    prefix=APIRoutes.CARDS,
    tags=[APIRoutes.CARDS.as_tag()]
)


@cards_mock_router.get('', response_model=GetCardsResponseSchema)
async def get_cards_view(query: Annotated[GetCardsQuerySchema, Depends(GetCardsQuerySchema.as_query)]):
    return loader.load_http("get_cards/default.json", GetCardsResponseSchema)


@cards_mock_router.get('/{card_id}', response_model=GetCardResponseSchema)
async def get_card_view(card_id: uuid.UUID):
    return loader.load_http("get_card/default.json", GetCardResponseSchema)


@cards_mock_router.post('', response_model=CreateCardResponseSchema)
async def create_card_view(request: CreateCardRequestSchema):
    return loader.load_http("create_card/default.json", CreateCardResponseSchema)
