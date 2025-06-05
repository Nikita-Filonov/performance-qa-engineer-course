import uuid

from fastapi import HTTPException

from services.gateway.apps.operations.schema.operations import (
    MakeFeeOperationRequestSchema,
    MakeTopUpOperationRequestSchema,
    MakeTransferOperationRequestSchema,
    MakeCashbackOperationRequestSchema,
    MakePurchaseOperationRequestSchema,
    MakeBillPaymentOperationRequestSchema,
    MakeCashWithdrawalOperationRequestSchema,
)
from services.operations.apps.operations.schema.operations.base import (
    GetOperationResponseSchema,
    GetOperationsQuerySchema,
    GetOperationsResponseSchema,
    CreateOperationResponseSchema,
    GetOperationReceiptResponseSchema,
    GetOperationsSummaryQuerySchema,
    GetOperationsSummaryResponseSchema,
)
from services.operations.clients.operations.http import (
    OperationsHTTPClient,
    OperationsHTTPClientError
)


async def get_operation(
        operation_id: uuid.UUID,
        operations_http_client: OperationsHTTPClient
) -> GetOperationResponseSchema:
    try:
        return await operations_http_client.get_operation(operation_id)
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Get operation: {error.details}",
            status_code=error.status_code
        )


async def get_operations(
        query: GetOperationsQuerySchema,
        operations_http_client: OperationsHTTPClient
) -> GetOperationsResponseSchema:
    return await operations_http_client.get_operations(account_id=query.account_id)


async def get_operation_receipt(
        operation_id: uuid.UUID,
        operations_http_client: OperationsHTTPClient
) -> GetOperationReceiptResponseSchema:
    try:
        return await operations_http_client.get_operation_receipt(operation_id)
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Get operation receipt: {error.details}",
            status_code=error.status_code
        )


async def get_operations_summary(
        query: GetOperationsSummaryQuerySchema,
        operations_http_client: OperationsHTTPClient
) -> GetOperationsSummaryResponseSchema:
    return await operations_http_client.get_operations_summary(account_id=query.account_id)


async def make_fee_operation(
        request: MakeFeeOperationRequestSchema,
        operations_http_client: OperationsHTTPClient
) -> CreateOperationResponseSchema:
    try:
        return await operations_http_client.make_fee_operation(**request.model_dump())
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Make fee operation: {error.details}",
            status_code=error.status_code
        )


async def make_top_up_operation(
        request: MakeTopUpOperationRequestSchema,
        operations_http_client: OperationsHTTPClient
) -> CreateOperationResponseSchema:
    try:
        return await operations_http_client.make_top_up_operation(**request.model_dump())
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Make top up operation: {error.details}",
            status_code=error.status_code
        )


async def make_purchase_operation(
        request: MakePurchaseOperationRequestSchema,
        operations_http_client: OperationsHTTPClient
) -> CreateOperationResponseSchema:
    try:
        return await operations_http_client.make_purchase_operation(**request.model_dump())
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Make purchase operation: {error.details}",
            status_code=error.status_code
        )


async def make_cashback_operation(
        request: MakeCashbackOperationRequestSchema,
        operations_http_client: OperationsHTTPClient
) -> CreateOperationResponseSchema:
    try:
        return await operations_http_client.make_cashback_operation(**request.model_dump())
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Make cashback operation: {error.details}",
            status_code=error.status_code
        )


async def make_transfer_operation(
        request: MakeTransferOperationRequestSchema,
        operations_http_client: OperationsHTTPClient
) -> CreateOperationResponseSchema:
    try:
        return await operations_http_client.make_transfer_operation(**request.model_dump())
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Make transfer operation: {error.details}",
            status_code=error.status_code
        )


async def make_bill_payment_operation(
        request: MakeBillPaymentOperationRequestSchema,
        operations_http_client: OperationsHTTPClient
) -> CreateOperationResponseSchema:
    try:
        return await operations_http_client.make_bill_payment_operation(**request.model_dump())
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Make bill payment operation: {error.details}",
            status_code=error.status_code
        )


async def make_cash_withdrawal_operation(
        request: MakeCashWithdrawalOperationRequestSchema,
        operations_http_client: OperationsHTTPClient
) -> CreateOperationResponseSchema:
    try:
        return await operations_http_client.make_cash_withdrawal_operation(**request.model_dump())
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Make cash withdrawal operation: {error.details}",
            status_code=error.status_code
        )
