from pydantic import HttpUrl, UUID4

from libs.schema.base import BaseSchema


class ReceiptSchema(BaseSchema):
    url: HttpUrl
    document: bytes


class GetReceiptResponseSchema(BaseSchema):
    receipt: ReceiptSchema


class CreateReceiptRequestSchema(BaseSchema):
    content: bytes
    operation_id: UUID4


class CreateReceiptResponseSchema(BaseSchema):
    receipt: ReceiptSchema
