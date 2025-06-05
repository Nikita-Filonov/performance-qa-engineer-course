from pydantic import HttpUrl, UUID4

from libs.schema.base import BaseSchema


class ContractSchema(BaseSchema):
    url: HttpUrl
    document: bytes


class GetContractResponseSchema(BaseSchema):
    contract: ContractSchema


class CreateContractRequestSchema(BaseSchema):
    content: bytes
    account_id: UUID4


class CreateContractResponseSchema(BaseSchema):
    contract: ContractSchema
