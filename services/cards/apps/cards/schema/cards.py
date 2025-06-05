from datetime import date
from typing import Self

from fastapi import Query
from pydantic import UUID4

from libs.schema.base import BaseSchema
from libs.schema.query import QuerySchema
from services.cards.services.postgres.models.cards import CardType, CardStatus, CardPaymentSystem


class CardSchema(BaseSchema):
    id: UUID4
    pin: str
    cvv: str
    type: CardType
    status: CardStatus
    account_id: UUID4
    card_number: str
    card_holder: str
    expiry_date: date
    payment_system: CardPaymentSystem


class GetCardResponseSchema(BaseSchema):
    card: CardSchema


class GetCardsQuerySchema(QuerySchema):
    account_id: UUID4

    @classmethod
    async def as_query(cls, account_id: UUID4 = Query(alias="accountId")) -> Self:
        return GetCardsQuerySchema(account_id=account_id)


class GetCardsResponseSchema(BaseSchema):
    cards: list[CardSchema]


class CreateCardRequestSchema(BaseSchema):
    pin: str
    cvv: str
    type: CardType
    status: CardStatus
    account_id: UUID4
    card_number: str
    card_holder: str
    expiry_date: date
    payment_system: CardPaymentSystem


class CreateCardResponseSchema(BaseSchema):
    card: CardSchema
