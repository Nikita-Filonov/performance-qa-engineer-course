import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.documents.clients.contracts.http import ContractsHTTPClient, get_contracts_http_client
from services.documents.clients.tariffs.http import TariffsHTTPClient, get_tariffs_http_client
from services.gateway.apps.documents.controllers.documents.http import get_tariff_document, get_contract_document
from services.gateway.apps.documents.schema.documents import (
    GetTariffDocumentResponseSchema,
    GetContractDocumentResponseSchema
)
from services.gateway.services.documents.redis.client import (
    GatewayDocumentsRedisClient,
    get_gateway_documents_redis_client
)

documents_gateway_router = APIRouter(
    prefix=APIRoutes.DOCUMENTS,
    tags=[APIRoutes.DOCUMENTS.as_tag()]
)


@documents_gateway_router.get(
    '/tariff-document/{account_id}',
    response_model=GetTariffDocumentResponseSchema
)
async def get_tariff_document_view(
        account_id: uuid.UUID,
        tariffs_http_client: Annotated[TariffsHTTPClient, Depends(get_tariffs_http_client)],
        gateway_documents_redis_client: Annotated[
            GatewayDocumentsRedisClient, Depends(get_gateway_documents_redis_client)
        ]
):
    return await get_tariff_document(
        account_id=account_id,
        tariffs_http_client=tariffs_http_client,
        gateway_documents_redis_client=gateway_documents_redis_client
    )


@documents_gateway_router.get(
    '/contract-document/{account_id}',
    response_model=GetContractDocumentResponseSchema
)
async def get_contract_document_view(
        account_id: uuid.UUID,
        contracts_http_client: Annotated[ContractsHTTPClient, Depends(get_contracts_http_client)],
        gateway_documents_redis_client: Annotated[
            GatewayDocumentsRedisClient, Depends(get_gateway_documents_redis_client)
        ]
):
    return await get_contract_document(
        account_id=account_id,
        contracts_http_client=contracts_http_client,
        gateway_documents_redis_client=gateway_documents_redis_client
    )
