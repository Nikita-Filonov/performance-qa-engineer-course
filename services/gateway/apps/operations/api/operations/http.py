import uuid
from typing import Annotated

from fastapi import Depends, APIRouter

from libs.routes import APIRoutes
from services.gateway.apps.operations.controllers.operations.http import (
    get_operation,
    get_operations,
    get_operation_receipt,
    get_operations_summary,
    make_fee_operation,
    make_top_up_operation,
    make_purchase_operation,
    make_cashback_operation,
    make_transfer_operation,
    make_bill_payment_operation,
    make_cash_withdrawal_operation
)
from services.gateway.apps.operations.schema.operations import (
    MakeFeeOperationRequestSchema,
    MakeTopUpOperationRequestSchema,
    MakePurchaseOperationRequestSchema,
    MakeCashbackOperationRequestSchema,
    MakeTransferOperationRequestSchema,
    MakeBillPaymentOperationRequestSchema,
    MakeCashWithdrawalOperationRequestSchema
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
from services.operations.clients.operations.http import OperationsHTTPClient, get_operations_http_client

operations_gateway_router = APIRouter(
    prefix=APIRoutes.OPERATIONS,
    tags=[APIRoutes.OPERATIONS.as_tag()]
)


@operations_gateway_router.get('', response_model=GetOperationsResponseSchema)
async def get_operations_view(
        query: Annotated[GetOperationsQuerySchema, Depends(GetOperationsQuerySchema.as_query)],
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await get_operations(query, operations_http_client)


@operations_gateway_router.get(
    '/operations-summary',
    response_model=GetOperationsSummaryResponseSchema
)
async def get_operations_summary_view(
        query: Annotated[
            GetOperationsSummaryQuerySchema, Depends(GetOperationsSummaryQuerySchema.as_query)
        ],
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await get_operations_summary(query, operations_http_client)


@operations_gateway_router.get(
    '/operation-receipt/{operation_id}',
    response_model=GetOperationReceiptResponseSchema
)
async def get_operation_receipt_view(
        operation_id: uuid.UUID,
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await get_operation_receipt(operation_id, operations_http_client)


@operations_gateway_router.get('/{operation_id}', response_model=GetOperationResponseSchema)
async def get_operation_view(
        operation_id: uuid.UUID,
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await get_operation(operation_id, operations_http_client)


@operations_gateway_router.post(
    '/make-fee-operation',
    response_model=CreateOperationResponseSchema
)
async def make_fee_operation_view(
        request: MakeFeeOperationRequestSchema,
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await make_fee_operation(request, operations_http_client)


@operations_gateway_router.post(
    '/make-top-up-operation',
    response_model=CreateOperationResponseSchema
)
async def make_top_up_operation_view(
        request: MakeTopUpOperationRequestSchema,
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await make_top_up_operation(request, operations_http_client)


@operations_gateway_router.post(
    '/make-cashback-operation',
    response_model=CreateOperationResponseSchema
)
async def make_cashback_operation_view(
        request: MakeCashbackOperationRequestSchema,
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await make_cashback_operation(request, operations_http_client)


@operations_gateway_router.post(
    '/make-transfer-operation',
    response_model=CreateOperationResponseSchema
)
async def make_transfer_operation_view(
        request: MakeTransferOperationRequestSchema,
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await make_transfer_operation(request, operations_http_client)


@operations_gateway_router.post(
    '/make-purchase-operation',
    response_model=CreateOperationResponseSchema
)
async def make_purchase_operation_view(
        request: MakePurchaseOperationRequestSchema,
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await make_purchase_operation(request, operations_http_client)


@operations_gateway_router.post(
    '/make-bill-payment-operation',
    response_model=CreateOperationResponseSchema
)
async def make_bill_payment_operation_view(
        request: MakeBillPaymentOperationRequestSchema,
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await make_bill_payment_operation(request, operations_http_client)


@operations_gateway_router.post(
    '/make-cash-withdrawal-operation',
    response_model=CreateOperationResponseSchema
)
async def make_cash_withdrawal_operation_view(
        request: MakeCashWithdrawalOperationRequestSchema,
        operations_http_client: Annotated[
            OperationsHTTPClient, Depends(get_operations_http_client)
        ],
):
    return await make_cash_withdrawal_operation(request, operations_http_client)
