import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.accounts.clients.accounts.http import AccountsHTTPClient, get_accounts_http_client
from services.cards.clients.cards.http import CardsHTTPClient, get_cards_http_client
from services.operations.apps.operations.controllers.operations.http import (
    get_operation,
    get_operations,
    create_operation,
    get_operation_receipt,
    get_operations_summary
)
from services.operations.apps.operations.schema.operations.base import (
    GetOperationResponseSchema,
    GetOperationsQuerySchema,
    GetOperationsResponseSchema,
    CreateOperationRequestSchema,
    CreateOperationResponseSchema,
    GetOperationReceiptResponseSchema,
    GetOperationsSummaryQuerySchema,
    GetOperationsSummaryResponseSchema,
)
from services.operations.services.postgres.repositories.operations import OperationsRepository, \
    get_operations_repository_depends
from services.operations.services.s3.client import OperationsS3Client, get_operations_s3_client
from services.payments.clients.payments.http import get_payments_http_client, PaymentsHTTPClient

operations_router = APIRouter(
    prefix=APIRoutes.OPERATIONS,
    tags=[APIRoutes.OPERATIONS.as_tag()]
)


@operations_router.get('', response_model=GetOperationsResponseSchema)
async def get_operations_view(
        query: Annotated[GetOperationsQuerySchema, Depends(GetOperationsQuerySchema.as_query)],
        operations_repository: Annotated[
            OperationsRepository, Depends(get_operations_repository_depends)
        ],
):
    return await get_operations(query, operations_repository)


@operations_router.get(
    '/operation-receipt/{operation_id}',
    response_model=GetOperationReceiptResponseSchema
)
async def get_operation_receipt_view(
        operation_id: uuid.UUID,
        operations_s3_client: Annotated[OperationsS3Client, Depends(get_operations_s3_client)],
        operations_repository: Annotated[
            OperationsRepository, Depends(get_operations_repository_depends)
        ],
):
    return await get_operation_receipt(
        operation_id=operation_id,
        operations_s3_client=operations_s3_client,
        operations_repository=operations_repository
    )


@operations_router.get(
    '/operations-summary',
    response_model=GetOperationsSummaryResponseSchema
)
async def get_operation_receipt_view(
        query: Annotated[
            GetOperationsSummaryQuerySchema, Depends(GetOperationsSummaryQuerySchema.as_query)
        ],
        operations_repository: Annotated[
            OperationsRepository, Depends(get_operations_repository_depends)
        ],
):
    return await get_operations_summary(query, operations_repository)


@operations_router.get('/{operation_id}', response_model=GetOperationResponseSchema)
async def get_operation_view(
        operation_id: uuid.UUID,
        operations_repository: Annotated[
            OperationsRepository, Depends(get_operations_repository_depends)
        ],
):
    return await get_operation(operation_id, operations_repository)


@operations_router.post('', response_model=CreateOperationResponseSchema)
async def create_operation_view(
        request: CreateOperationRequestSchema,
        cards_http_client: Annotated[CardsHTTPClient, Depends(get_cards_http_client)],
        payments_http_client: Annotated[PaymentsHTTPClient, Depends(get_payments_http_client)],
        accounts_http_client: Annotated[AccountsHTTPClient, Depends(get_accounts_http_client)],
        operations_s3_client: Annotated[OperationsS3Client, Depends(get_operations_s3_client)],
        operations_repository: Annotated[
            OperationsRepository, Depends(get_operations_repository_depends)
        ],
):
    return await create_operation(
        request=request,
        cards_http_client=cards_http_client,
        payments_http_client=payments_http_client,
        accounts_http_client=accounts_http_client,
        operations_s3_client=operations_s3_client,
        operations_repository=operations_repository
    )
