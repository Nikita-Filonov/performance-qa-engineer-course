from typing import AsyncGenerator, Any

from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from libs.postgres.engine import get_postgres_engine


async def get_users_database_session() -> AsyncGenerator[AsyncSession, Any]:
    session_factory = await get_postgres_engine(settings.users_postgres_database)

    async with session_factory() as session:
        yield session
