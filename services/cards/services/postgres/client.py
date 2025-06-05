from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from libs.postgres.engine import get_postgres_engine


async def get_cards_database_session() -> AsyncGenerator[AsyncSession, Any]:
    async_session = await get_postgres_engine(settings.cards_postgres_database)

    async with async_session() as session:
        yield session
