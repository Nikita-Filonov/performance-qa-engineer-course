import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from typing import Annotated, TypedDict, AsyncGenerator, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from libs.postgres.repository import BasePostgresRepository
from services.operations.services.postgres.client import get_operations_database_session
from services.operations.services.postgres.models.operations import (
    OperationType,
    OperationStatus,
    OperationsModel,
)


@dataclass
class OperationsSummary:
    spent_amount: float = 0.0
    received_amount: float = 0.0
    cashback_amount: float = 0.0


class CreateOperationDict(TypedDict):
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: uuid.UUID
    category: str
    created_at: datetime
    account_id: uuid.UUID


class OperationsRepository(BasePostgresRepository):
    model = OperationsModel

    async def get_by_id(self, operation_id: uuid.UUID) -> OperationsModel | None:
        return await self.model.get(
            self.session, clause_filter=(self.model.id == operation_id,)
        )

    async def filter(self, account_id: uuid.UUID) -> Sequence[OperationsModel]:
        return await self.model.filter(
            self.session, clause_filter=(self.model.account_id == account_id,)
        )

    async def create(self, data: CreateOperationDict) -> OperationsModel:
        return await self.model.create(self.session, **data)

    async def get_operations_summary(self, account_id: uuid.UUID) -> OperationsSummary:
        spent_amount = self.model.aggregate_amount_by_types(OperationType.list_spent())
        received_amount = self.model.aggregate_amount_by_types(OperationType.list_received())
        cashback_amount = self.model.aggregate_amount_by_types(OperationType.list_cashback())

        query = (
            select(
                spent_amount.label('spent_amount'),
                received_amount.label('received_amount'),
                cashback_amount.label('cashback_amount')
            )
            .where(
                self.model.account_id == account_id,
                self.model.status.in_([OperationStatus.COMPLETED, OperationStatus.IN_PROGRESS]),
            )
        )

        result = await self.session.execute(query)
        row = result.one()

        return OperationsSummary(
            spent_amount=row.spent_amount,
            received_amount=row.received_amount,
            cashback_amount=row.cashback_amount,
        )


@asynccontextmanager
async def get_operations_repository_context() -> AsyncGenerator[OperationsRepository, None]:
    async for session in get_operations_database_session():
        yield OperationsRepository(session=session)


async def get_operations_repository_depends(
        session: Annotated[AsyncSession, Depends(get_operations_database_session)]
) -> OperationsRepository:
    return OperationsRepository(session=session)
