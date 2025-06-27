from datetime import datetime
from typing import Self

from fastapi import Query
from pydantic import UUID4

from libs.schema.base import BaseSchema
from libs.schema.query import QuerySchema
from services.operations.apps.operations.schema.operations.operation import OperationSchema
from services.operations.apps.operations.schema.operations.operations_summary import OperationsSummarySchema
from services.operations.services.postgres.models.operations import OperationType, OperationStatus


class GetOperationResponseSchema(BaseSchema):
    operation: OperationSchema


class GetOperationsQuerySchema(QuerySchema):
    account_id: UUID4

    @classmethod
    async def as_query(cls, account_id: UUID4 = Query(alias="accountId")) -> Self:
        return GetOperationsSummaryQuerySchema(account_id=account_id)


class GetOperationsResponseSchema(BaseSchema):
    operations: list[OperationSchema]


class CreateOperationRequestSchema(BaseSchema):
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: UUID4
    category: str
    created_at: datetime
    account_id: UUID4


class CreateOperationResponseSchema(BaseSchema):
    operation: OperationSchema


class GetOperationsSummaryQuerySchema(QuerySchema):
    account_id: UUID4

    @classmethod
    async def as_query(cls, account_id: UUID4 = Query(alias="accountId")) -> Self:
        return GetOperationsSummaryQuerySchema(account_id=account_id)


class GetOperationsSummaryResponseSchema(BaseSchema):
    summary: OperationsSummarySchema
