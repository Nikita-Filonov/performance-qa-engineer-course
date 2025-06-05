from datetime import datetime

from pydantic import UUID4

from libs.schema.base import BaseSchema
from services.operations.services.postgres.models.operations import OperationType, OperationStatus


class OperationSchema(BaseSchema):
    id: UUID4
    type: OperationType
    status: OperationStatus
    amount: float
    card_id: UUID4
    category: str
    created_at: datetime
    account_id: UUID4
