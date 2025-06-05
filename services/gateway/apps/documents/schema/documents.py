from libs.schema.base import BaseSchema
from services.documents.apps.contracts.schema.contracts import ContractSchema
from services.documents.apps.tariffs.schema.tariffs import TariffSchema


class GetTariffDocumentResponseSchema(BaseSchema):
    tariff: TariffSchema


class GetContractDocumentResponseSchema(BaseSchema):
    contract: ContractSchema
