import uuid

from fastapi import APIRouter

from libs.routes import APIRoutes
from services.documents.apps.contracts.schema.contracts import (
    GetContractResponseSchema,
    CreateContractRequestSchema,
    CreateContractResponseSchema
)
from services.mock.apps.documents.contracts.mock import loader

contracts_mock_router = APIRouter(
    prefix=APIRoutes.CONTRACTS,
    tags=[APIRoutes.CONTRACTS.as_tag()]
)


@contracts_mock_router.get('/{account_id}', response_model=GetContractResponseSchema)
async def get_contract_view(account_id: uuid.UUID):
    return await loader.load_http_with_timeout("get_contract/default.json", GetContractResponseSchema)


@contracts_mock_router.post('', response_model=CreateContractResponseSchema)
async def create_contract_view(request: CreateContractRequestSchema):
    return await loader.load_http_with_timeout("create_contract/default.json", CreateContractResponseSchema)
