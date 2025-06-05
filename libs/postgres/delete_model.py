from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from libs.postgres.abstract_model import AbstractModel
from libs.postgres.query import build_query
from libs.postgres.types import ColumnExpressionType


class DeleteModel(AbstractModel):
    __abstract__ = True

    @classmethod
    async def delete(
            cls,
            session: AsyncSession,
            clause_filter: ColumnExpressionType,
            **kwargs
    ) -> None:
        query = delete(cls).filter_by(**kwargs)
        query = await build_query(query, clause_filter=clause_filter)

        await session.execute(query)
        await session.commit()
