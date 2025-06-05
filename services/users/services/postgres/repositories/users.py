import uuid
from contextlib import asynccontextmanager
from typing import Annotated, TypedDict, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from libs.postgres.repository import BasePostgresRepository
from services.users.services.postgres.client import get_users_database_session
from services.users.services.postgres.models.users import UsersModel


class CreateUserDict(TypedDict):
    email: str
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str


class UsersRepository(BasePostgresRepository):
    model = UsersModel

    async def get_by_id(self, user_id: uuid.UUID) -> UsersModel | None:
        return await self.model.get(
            self.session, clause_filter=(self.model.id == user_id,)
        )

    async def get_by_email(self, email: str) -> UsersModel | None:
        return await self.model.get(self.session, clause_filter=(self.model.email == email,))

    async def create(self, data: CreateUserDict) -> UsersModel:
        return await self.model.create(self.session, **data)

    async def update(self, user_id: uuid.UUID, data: dict) -> UsersModel:
        return await self.model.update(
            self.session, clause_filter=(self.model.id == user_id,), **data
        )

    async def delete(self, user_id: uuid.UUID) -> None:
        return await self.model.delete(self.session, clause_filter=(self.model.id == user_id,))


@asynccontextmanager
async def get_users_repository_context() -> AsyncGenerator[UsersRepository, None]:
    async for session in get_users_database_session():
        yield UsersRepository(session=session)


async def get_users_repository_depends(
        session: Annotated[AsyncSession, Depends(get_users_database_session)]
) -> UsersRepository:
    return UsersRepository(session=session)
