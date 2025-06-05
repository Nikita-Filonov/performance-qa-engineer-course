import uuid

from httpx import Response

from config import settings
from libs.http.client.base import HTTPClient
from libs.http.client.handlers import handle_http_error, HTTPClientError
from libs.logger import get_logger
from libs.routes import APIRoutes
from services.documents.apps.contracts.schema.contracts import (
    GetContractResponseSchema,
    CreateContractRequestSchema,
    CreateContractResponseSchema,
)


class ContractsHTTPClientError(HTTPClientError):
    pass


class ContractsHTTPClient(HTTPClient):
    @handle_http_error(client='ContractsHTTPClient', exception=ContractsHTTPClientError)
    async def get_contract_api(self, account_id: uuid.UUID) -> Response:
        return await self.get(f'{APIRoutes.CONTRACTS}/{account_id}')

    @handle_http_error(client='ContractsHTTPClient', exception=ContractsHTTPClientError)
    async def create_contract_api(self, request: CreateContractRequestSchema) -> Response:
        return await self.post(
            APIRoutes.CONTRACTS, json=request.model_dump(mode='json', by_alias=True)
        )

    async def get_contract(self, account_id: uuid.UUID) -> GetContractResponseSchema:
        response = await self.get_contract_api(account_id)
        return GetContractResponseSchema.model_validate_json(response.text)

    async def create_contract(
            self,
            account_id: uuid.UUID,
            content: bytes
    ) -> CreateContractResponseSchema:
        request = CreateContractRequestSchema(account_id=account_id, content=content)
        response = await self.create_contract_api(request)
        return CreateContractResponseSchema.model_validate_json(response.text)


def get_contracts_http_client() -> ContractsHTTPClient:
    logger = get_logger("CONTRACTS_SERVICE_HTTP_CLIENT")
    return ContractsHTTPClient(config=settings.documents_http_client, logger=logger)
