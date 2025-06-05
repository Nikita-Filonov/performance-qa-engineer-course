from libs.schema.base import BaseSchema


class OperationsSummarySchema(BaseSchema):
    spent_amount: float
    received_amount: float
    cashback_amount: float
