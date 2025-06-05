from typing import Self, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from libs.postgres.abstract_model import AbstractModel
from libs.postgres.query import build_query
from libs.postgres.types import ColumnExpressionType


class FilterModel(AbstractModel):
    __abstract__ = True

    @classmethod
    async def get(
            cls,
            session: AsyncSession,
            options: tuple[ExecutableOption, ...] | None = None,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> Self | None:
        query = select(cls).filter_by(**kwargs)
        query = await build_query(query, options=options, clause_filter=clause_filter)

        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def filter(
            cls,
            session: AsyncSession,
            limit: int | None = None,
            offset: int | None = None,
            options: tuple[ExecutableOption, ...] | None = None,
            distinct: ColumnExpressionType | None = None,
            order_by: ColumnExpressionType | None = None,
            clause_filter: ColumnExpressionType | None = None,
            **kwargs
    ) -> Sequence[Self]:
        query = select(cls).filter_by(**kwargs)
        query = await build_query(
            query,
            limit=limit,
            offset=offset,
            options=options,
            distinct=distinct,
            order_by=order_by,
            clause_filter=clause_filter
        )

        result = await session.execute(query)

        return result.scalars().all()
