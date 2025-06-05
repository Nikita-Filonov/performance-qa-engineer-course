from pydantic import UUID4

from libs.schema.base import BaseSchema
from services.operations.services.postgres.models.operations import OperationStatus


class MakeOperationRequestSchema(BaseSchema):
    status: OperationStatus
    amount: float
    card_id: UUID4
    account_id: UUID4


class MakeFeeOperationRequestSchema(MakeOperationRequestSchema):
    pass


class MakeTopUpOperationRequestSchema(MakeOperationRequestSchema):
    pass


class MakeTransferOperationRequestSchema(MakeOperationRequestSchema):
    pass


class MakeCashbackOperationRequestSchema(MakeOperationRequestSchema):
    pass


class MakePurchaseOperationRequestSchema(MakeOperationRequestSchema):
    category: str


class MakeBillPaymentOperationRequestSchema(MakeOperationRequestSchema):
    pass


class MakeCashWithdrawalOperationRequestSchema(MakeOperationRequestSchema):
    pass
