from pydantic import HttpUrl

from libs.schema.base import BaseSchema


class OperationReceiptSchema(BaseSchema):
    url: HttpUrl
    document: bytes
