from pydantic import HttpUrl, UUID4

from libs.schema.base import BaseSchema


class TariffSchema(BaseSchema):
    url: HttpUrl
    document: bytes


class GetTariffResponseSchema(BaseSchema):
    tariff: TariffSchema


class CreateTariffRequestSchema(BaseSchema):
    content: bytes
    account_id: UUID4


class CreateTariffResponseSchema(BaseSchema):
    tariff: TariffSchema
