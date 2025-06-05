from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from libs.postgres.abstract_model import AbstractModel
from libs.postgres.query import build_query
from libs.postgres.types import ColumnExpressionType


class UpdateModel(AbstractModel):
    __abstract__ = True

    @classmethod
    async def update(
            cls,
            session: AsyncSession,
            clause_filter: ColumnExpressionType,
            **kwargs
    ) -> Self | None:
        query = cls.__table__.update().values(**kwargs).returning(cls)
        query = await build_query(query, clause_filter=clause_filter)

        result = await session.execute(query)
        await session.commit()

        if result := result.mappings().first():
            return cls(**result)
