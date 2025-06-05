from contracts.services.documents.contracts.contract_pb2 import Contract
from contracts.services.documents.tariffs.tariff_pb2 import Tariff
from contracts.services.gateway.documents.rpc_get_contract_document_pb2 import (
    GetContractDocumentRequest,
    GetContractDocumentResponse
)
from contracts.services.gateway.documents.rpc_get_tariff_document_pb2 import (
    GetTariffDocumentRequest,
    GetTariffDocumentResponse
)
from libs.protobuf.tools import protobuf_to_json
from services.documents.clients.contracts.grpc import ContractsGRPCClient
from services.documents.clients.tariffs.grpc import TariffsGRPCClient
from services.gateway.services.documents.redis.client import GatewayDocumentsRedisClient


async def get_tariff_document(
        request: GetTariffDocumentRequest,
        tariffs_grpc_client: TariffsGRPCClient,
        gateway_documents_redis_client: GatewayDocumentsRedisClient
) -> GetTariffDocumentResponse:
    tariff_cache = await gateway_documents_redis_client.get_tariff_document(request.account_id)
    if tariff_cache:
        return GetTariffDocumentResponse(tariff=Tariff(**tariff_cache))

    tariff = await tariffs_grpc_client.get_tariff(request.account_id)
    await gateway_documents_redis_client.set_tariff_document(
        request.account_id, protobuf_to_json(tariff)
    )

    return GetTariffDocumentResponse(tariff=tariff)


async def get_contract_document(
        request: GetContractDocumentRequest,
        contracts_grpc_client: ContractsGRPCClient,
        gateway_documents_redis_client: GatewayDocumentsRedisClient
) -> GetContractDocumentResponse:
    contract_cache = await gateway_documents_redis_client.get_contract_document(request.account_id)
    if contract_cache:
        return GetContractDocumentResponse(contract=Contract(**contract_cache))

    contract = await contracts_grpc_client.get_contract(request.account_id)
    await gateway_documents_redis_client.set_contract_document(
        request.account_id, protobuf_to_json(contract)
    )

    return GetContractDocumentResponse(contract=contract)
