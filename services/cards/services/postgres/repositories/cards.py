import uuid
from contextlib import asynccontextmanager
from datetime import date
from typing import Annotated, TypedDict, AsyncGenerator, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from libs.postgres.repository import BasePostgresRepository
from services.cards.services.postgres.client import get_cards_database_session
from services.cards.services.postgres.models.cards import (
    CardType,
    CardStatus,
    CardsModel,
    CardPaymentSystem
)


class CreateCardDict(TypedDict):
    pin: str
    cvv: str
    type: CardType
    status: CardStatus
    account_id: uuid.UUID
    card_number: str
    card_holder: str
    expiry_date: date
    payment_system: CardPaymentSystem


class CardsRepository(BasePostgresRepository):
    model = CardsModel

    async def get_by_id(self, card_id: uuid.UUID) -> CardsModel | None:
        return await self.model.get(
            self.session, clause_filter=(self.model.id == card_id,)
        )

    async def filter(self, account_id: uuid.UUID) -> Sequence[CardsModel]:
        return await self.model.filter(
            self.session, clause_filter=(self.model.account_id == account_id,)
        )

    async def create(self, data: CreateCardDict) -> CardsModel:
        return await self.model.create(self.session, **data)

    async def update(self, card_id: uuid.UUID, data: dict) -> CardsModel:
        return await self.model.update(
            self.session, clause_filter=(self.model.id == card_id,), **data
        )


@asynccontextmanager
async def get_cards_repository_context() -> AsyncGenerator[CardsRepository, None]:
    async for session in get_cards_database_session():
        yield CardsRepository(session=session)


async def get_cards_repository_depends(
        session: Annotated[AsyncSession, Depends(get_cards_database_session)]
) -> CardsRepository:
    return CardsRepository(session=session)
