from typing import TypedDict, Any

from config import settings
from libs.logger import get_logger
from libs.redis.client import RedisClient


class TariffDocumentDict(TypedDict):
    url: str
    document: bytes


class ContractDocumentDict(TypedDict):
    url: str
    document: bytes


def build_tariff_document_key(account_id: str) -> str:
    return f'tariff_{account_id}'


def build_contract_document_key(account_id: str) -> str:
    return f'contract_{account_id}'


def normalize_tariff_document(value: Any | None) -> TariffDocumentDict | None:
    return TariffDocumentDict(
        url=value['url'],
        document=value['document'].encode()
    ) if value else None


def normalize_contract_document(value: Any | None) -> ContractDocumentDict | None:
    return ContractDocumentDict(
        url=value['url'],
        document=value['document'].encode()
    ) if value else None


class GatewayDocumentsRedisClient(RedisClient):
    async def set_tariff_document(self, account_id: str, document: str):
        await self.set(
            key=build_tariff_document_key(account_id),
            value=document
        )

    async def get_tariff_document(self, account_id: str) -> TariffDocumentDict | None:
        result = await self.get_json(key=build_tariff_document_key(account_id))
        return normalize_tariff_document(result)

    async def set_contract_document(self, account_id: str, document: str):
        await self.set(
            key=build_contract_document_key(account_id),
            value=document
        )

    async def get_contract_document(self, account_id: str) -> ContractDocumentDict | None:
        result = await self.get_json(key=build_contract_document_key(account_id))
        return normalize_contract_document(result)


def get_gateway_documents_redis_client() -> GatewayDocumentsRedisClient:
    logger = get_logger("GATEWAY_DOCUMENTS_REDIS_CLIENT")
    return GatewayDocumentsRedisClient(
        prefix="gateway-service.documents",
        logger=logger,
        config=settings.gateway_redis_client
    )
