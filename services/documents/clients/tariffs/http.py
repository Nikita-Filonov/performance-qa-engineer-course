import uuid

from httpx import Response

from config import settings
from libs.http.client.base import HTTPClient
from libs.http.client.handlers import handle_http_error, HTTPClientError
from libs.logger import get_logger
from libs.routes import APIRoutes
from services.documents.apps.tariffs.schema.tariffs import (
    GetTariffResponseSchema,
    CreateTariffRequestSchema,
    CreateTariffResponseSchema
)


class TariffsHTTPClientError(HTTPClientError):
    pass


class TariffsHTTPClient(HTTPClient):
    @handle_http_error(client='TariffsHTTPClient', exception=TariffsHTTPClientError)
    async def get_tariff_api(self, account_id: uuid.UUID) -> Response:
        return await self.get(f'{APIRoutes.TARIFFS}/{account_id}')

    @handle_http_error(client='TariffsHTTPClient', exception=TariffsHTTPClientError)
    async def create_tariff_api(self, request: CreateTariffRequestSchema) -> Response:
        return await self.post(
            APIRoutes.TARIFFS, json=request.model_dump(mode='json', by_alias=True)
        )

    async def get_tariff(self, account_id: uuid.UUID) -> GetTariffResponseSchema:
        response = await self.get_tariff_api(account_id)
        return GetTariffResponseSchema.model_validate_json(response.text)

    async def create_tariff(
            self,
            account_id: uuid.UUID,
            content: bytes
    ) -> CreateTariffResponseSchema:
        request = CreateTariffRequestSchema(account_id=account_id, content=content)
        response = await self.create_tariff_api(request)
        return CreateTariffResponseSchema.model_validate_json(response.text)


def get_tariffs_http_client() -> TariffsHTTPClient:
    logger = get_logger("TARIFFS_SERVICE_HTTP_CLIENT")
    return TariffsHTTPClient(config=settings.documents_http_client, logger=logger)
