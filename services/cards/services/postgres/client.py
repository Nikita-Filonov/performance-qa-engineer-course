from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from libs.postgres.engine import get_postgres_engine

session_factory = get_postgres_engine(settings.cards_postgres_database)


async def get_cards_database_session() -> AsyncGenerator[AsyncSession, Any]:
    async with session_factory() as session:
        yield session
