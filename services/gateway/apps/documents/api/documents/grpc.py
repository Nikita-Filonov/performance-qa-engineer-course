from grpc.aio import ServicerContext

from contracts.services.gateway.documents.documents_gateway_service_pb2_grpc import DocumentsGatewayServiceServicer
from contracts.services.gateway.documents.rpc_get_contract_document_pb2 import (
    GetContractDocumentRequest,
    GetContractDocumentResponse
)
from contracts.services.gateway.documents.rpc_get_tariff_document_pb2 import (
    GetTariffDocumentRequest,
    GetTariffDocumentResponse
)
from services.documents.clients.contracts.grpc import get_contracts_grpc_client
from services.documents.clients.tariffs.grpc import get_tariffs_grpc_client
from services.gateway.apps.documents.controllers.documents.grpc import get_tariff_document, get_contract_document
from services.gateway.services.documents.redis.client import get_gateway_documents_redis_client


class DocumentsGatewayService(DocumentsGatewayServiceServicer):
    async def GetTariffDocument(
            self,
            request: GetTariffDocumentRequest,
            context: ServicerContext
    ) -> GetTariffDocumentResponse:
        return await get_tariff_document(
            request,
            tariffs_grpc_client=get_tariffs_grpc_client(),
            gateway_documents_redis_client=get_gateway_documents_redis_client()
        )

    async def GetContractDocument(
            self,
            request: GetContractDocumentRequest,
            context: ServicerContext
    ) -> GetContractDocumentResponse:
        return await get_contract_document(
            request,
            contracts_grpc_client=get_contracts_grpc_client(),
            gateway_documents_redis_client=get_gateway_documents_redis_client()
        )
