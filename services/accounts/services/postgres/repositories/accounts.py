import uuid
from contextlib import asynccontextmanager
from typing import Annotated, TypedDict, Sequence

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from libs.postgres.repository import BasePostgresRepository
from services.accounts.services.postgres.client import get_accounts_database_session
from services.accounts.services.postgres.models.accounts import AccountsModel, AccountType, AccountStatus


class CreateAccountDict(TypedDict):
    type: AccountType
    status: AccountStatus
    user_id: uuid.UUID
    balance: float


class UpdateAccountDict(TypedDict, total=False):
    type: AccountType
    status: AccountStatus
    user_id: uuid.UUID
    balance: float


class AccountsRepository(BasePostgresRepository):
    model = AccountsModel

    async def get_by_id(self, account_id: uuid.UUID) -> AccountsModel | None:
        return await self.model.get(
            self.session, clause_filter=(self.model.id == account_id,)
        )

    async def filter(self, user_id: uuid.UUID) -> Sequence[AccountsModel]:
        return await self.model.filter(
            self.session, clause_filter=(self.model.user_id == user_id,)
        )

    async def create(self, data: CreateAccountDict) -> AccountsModel:
        return await self.model.create(self.session, **data)

    async def update(self, account_id: uuid.UUID, data: UpdateAccountDict) -> AccountsModel:
        return await self.model.update(
            self.session, clause_filter=(self.model.id == account_id,), **data
        )


@asynccontextmanager
async def get_accounts_repository_context() -> AccountsRepository:
    async for session in get_accounts_database_session():
        yield AccountsRepository(session=session)


async def get_accounts_repository_depends(
        session: Annotated[AsyncSession, Depends(get_accounts_database_session)]
) -> AccountsRepository:
    return AccountsRepository(session=session)
