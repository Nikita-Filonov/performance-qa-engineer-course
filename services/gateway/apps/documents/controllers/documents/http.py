import uuid

from services.documents.apps.contracts.schema.contracts import ContractSchema
from services.documents.apps.tariffs.schema.tariffs import TariffSchema
from services.documents.clients.contracts.http import ContractsHTTPClient
from services.documents.clients.tariffs.http import TariffsHTTPClient
from services.gateway.apps.documents.schema.documents import (
    GetTariffDocumentResponseSchema,
    GetContractDocumentResponseSchema
)
from services.gateway.services.documents.redis.client import GatewayDocumentsRedisClient


async def get_tariff_document(
        account_id: uuid.UUID,
        tariffs_http_client: TariffsHTTPClient,
        gateway_documents_redis_client: GatewayDocumentsRedisClient
) -> GetTariffDocumentResponseSchema:
    tariff_cache = await gateway_documents_redis_client.get_tariff_document(str(account_id))
    if tariff_cache:
        return GetTariffDocumentResponseSchema(tariff=TariffSchema(**tariff_cache))

    get_tariff_response = await tariffs_http_client.get_tariff(account_id)
    await gateway_documents_redis_client.set_tariff_document(
        str(account_id), get_tariff_response.tariff.model_dump_json()
    )

    return GetTariffDocumentResponseSchema(tariff=get_tariff_response.tariff)


async def get_contract_document(
        account_id: uuid.UUID,
        contracts_http_client: ContractsHTTPClient,
        gateway_documents_redis_client: GatewayDocumentsRedisClient
) -> GetContractDocumentResponseSchema:
    contract_cache = await gateway_documents_redis_client.get_contract_document(str(account_id))
    if contract_cache:
        return GetContractDocumentResponseSchema(contract=ContractSchema(**contract_cache))

    get_contract_response = await contracts_http_client.get_contract(account_id)
    await gateway_documents_redis_client.set_contract_document(
        str(account_id), get_contract_response.contract.model_dump_json()
    )

    return GetContractDocumentResponseSchema(contract=get_contract_response.contract)
