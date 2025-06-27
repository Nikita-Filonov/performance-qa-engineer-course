import uuid
from datetime import datetime

from httpx import Response, QueryParams

from config import settings
from libs.http.client.base import HTTPClient
from libs.http.client.handlers import handle_http_error, HTTPClientError
from libs.logger import get_logger
from libs.routes import APIRoutes
from services.operations.apps.operations.schema.operations.base import (
    GetOperationResponseSchema,
    GetOperationsQuerySchema,
    GetOperationsResponseSchema,
    CreateOperationRequestSchema,
    CreateOperationResponseSchema,
    GetOperationsSummaryQuerySchema,
    GetOperationsSummaryResponseSchema,
)
from services.operations.clients.operations.base import positive_amount, negative_amount, Category
from services.operations.services.postgres.models.operations import OperationType, OperationStatus


class OperationsHTTPClientError(HTTPClientError):
    pass


class OperationsHTTPClient(HTTPClient):
    @handle_http_error(client='OperationsHTTPClient', exception=OperationsHTTPClientError)
    async def get_operation_api(self, operation_id: uuid.UUID) -> Response:
        return await self.get(f'{APIRoutes.OPERATIONS}/{operation_id}')

    @handle_http_error(client='OperationsHTTPClient', exception=OperationsHTTPClientError)
    async def get_operations_api(self, query: GetOperationsQuerySchema) -> Response:
        return await self.get(
            APIRoutes.OPERATIONS,
            params=QueryParams(**query.model_dump(mode='json', by_alias=True))
        )

    @handle_http_error(client='OperationsHTTPClient', exception=OperationsHTTPClientError)
    async def create_operation_api(self, request: CreateOperationRequestSchema) -> Response:
        return await self.post(
            APIRoutes.OPERATIONS, json=request.model_dump(mode='json', by_alias=True)
        )

    @handle_http_error(client='OperationsHTTPClient', exception=OperationsHTTPClientError)
    async def get_operations_summary_api(self, query: GetOperationsSummaryQuerySchema) -> Response:
        return await self.get(
            f'{APIRoutes.OPERATIONS}/operations-summary',
            params=QueryParams(**query.model_dump(mode='json', by_alias=True))
        )

    async def get_operation(self, operation_id: uuid.UUID) -> GetOperationResponseSchema:
        response = await self.get_operation_api(operation_id)
        return GetOperationResponseSchema.model_validate_json(response.text)

    async def get_operations(self, account_id: uuid.UUID) -> GetOperationsResponseSchema:
        query = GetOperationsQuerySchema(account_id=account_id)
        response = await self.get_operations_api(query)
        return GetOperationsResponseSchema.model_validate_json(response.text)

    async def make_fee_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: uuid.UUID,
            account_id: uuid.UUID,
    ) -> CreateOperationResponseSchema:
        request = CreateOperationRequestSchema(
            type=OperationType.FEE,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=Category.FEE,
            created_at=datetime.now(),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    async def make_top_up_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> CreateOperationResponseSchema:
        request = CreateOperationRequestSchema(
            type=OperationType.TOP_UP,
            status=status,
            amount=positive_amount(amount),
            card_id=card_id,
            category=Category.MONEY_IN,
            created_at=datetime.now(),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    async def make_purchase_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            category: str,
            account_id: str
    ) -> CreateOperationResponseSchema:
        request = CreateOperationRequestSchema(
            type=OperationType.PURCHASE,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=category,
            created_at=datetime.now(),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    async def make_cashback_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> CreateOperationResponseSchema:
        request = CreateOperationRequestSchema(
            type=OperationType.CASHBACK,
            status=status,
            amount=positive_amount(amount),
            card_id=card_id,
            category=Category.CASHBACK_REWARDS,
            created_at=datetime.now(),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    async def make_transfer_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> CreateOperationResponseSchema:
        request = CreateOperationRequestSchema(
            type=OperationType.TRANSFER,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=Category.TRANSFER,
            created_at=datetime.now(),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    async def make_bill_payment_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> CreateOperationResponseSchema:
        request = CreateOperationRequestSchema(
            type=OperationType.BILL_PAYMENT,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=Category.BILL_PAYMENT,
            created_at=datetime.now(),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    async def make_cash_withdrawal_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> CreateOperationResponseSchema:
        request = CreateOperationRequestSchema(
            type=OperationType.CASH_WITHDRAWAL,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=Category.CASH_WITHDRAWAL,
            created_at=datetime.now(),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return CreateOperationResponseSchema.model_validate_json(response.text)

    async def get_operations_summary(
            self,
            account_id: uuid.UUID
    ) -> GetOperationsSummaryResponseSchema:
        query = GetOperationsSummaryQuerySchema(account_id=account_id)
        response = await self.get_operations_summary_api(query)
        return GetOperationsSummaryResponseSchema.model_validate_json(response.text)


def get_operations_http_client() -> OperationsHTTPClient:
    logger = get_logger("OPERATIONS_SERVICE_HTTP_CLIENT")
    return OperationsHTTPClient(config=settings.operations_http_client, logger=logger)
