from datetime import date
from enum import StrEnum

from pydantic import UUID4

from libs.schema.base import BaseSchema


class PaymentStatus(StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    AUTHORIZED = "AUTHORIZED"
    CAPTURED = "CAPTURED"
    REFUNDED = "REFUNDED"
    DECLINED = "DECLINED"
    FAILED = "FAILED"


class PaymentSystem(StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    MASTERCARD = "MASTERCARD"
    VISA = "VISA"


class PaymentSchema(BaseSchema):
    id: UUID4
    status: PaymentStatus
    system: PaymentSystem
    message: str


class RefundPaymentRequestSchema(BaseSchema):
    amount: float
    system: PaymentSystem
    payment_id: UUID4


class RefundPaymentResponseSchema(BaseSchema):
    payment: PaymentSchema


class CapturePaymentRequestSchema(BaseSchema):
    system: PaymentSystem
    payment_id: UUID4


class CapturePaymentResponseSchema(BaseSchema):
    payment: PaymentSchema


class AuthorizePaymentRequestSchema(BaseSchema):
    cvv: str
    amount: float
    system: PaymentSystem
    expiry_date: date
    card_number: str
    card_holder: str


class AuthorizePaymentResponseSchema(BaseSchema):
    payment: PaymentSchema
