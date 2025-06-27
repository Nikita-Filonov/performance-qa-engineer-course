import uuid

from httpx import Response

from config import settings
from libs.http.client.base import HTTPClient
from libs.http.client.handlers import handle_http_error, HTTPClientError
from libs.logger import get_logger
from libs.routes import APIRoutes
from services.documents.apps.receipts.schema.receipts import (
    GetReceiptResponseSchema,
    CreateReceiptRequestSchema,
    CreateReceiptResponseSchema
)


class ReceiptsHTTPClientError(HTTPClientError):
    pass


class ReceiptsHTTPClient(HTTPClient):
    @handle_http_error(client='ReceiptsHTTPClient', exception=ReceiptsHTTPClientError)
    async def get_receipt_api(self, account_id: uuid.UUID) -> Response:
        return await self.get(f'{APIRoutes.RECEIPTS}/{account_id}')

    @handle_http_error(client='ReceiptsHTTPClient', exception=ReceiptsHTTPClientError)
    async def create_receipt_api(self, request: CreateReceiptRequestSchema) -> Response:
        return await self.post(
            APIRoutes.RECEIPTS, json=request.model_dump(mode='json', by_alias=True)
        )

    async def get_receipt(self, account_id: uuid.UUID) -> GetReceiptResponseSchema:
        response = await self.get_receipt_api(account_id)
        return GetReceiptResponseSchema.model_validate_json(response.text)

    async def create_receipt(
            self,
            operation_id: uuid.UUID,
            content: bytes
    ) -> CreateReceiptResponseSchema:
        request = CreateReceiptRequestSchema(operation_id=operation_id, content=content)
        response = await self.create_receipt_api(request)
        return CreateReceiptResponseSchema.model_validate_json(response.text)


def get_receipts_http_client() -> ReceiptsHTTPClient:
    logger = get_logger("RECEIPTS_SERVICE_HTTP_CLIENT")
    return ReceiptsHTTPClient(config=settings.documents_http_client, logger=logger)
