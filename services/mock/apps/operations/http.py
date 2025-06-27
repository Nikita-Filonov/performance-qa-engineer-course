import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.mock.apps.operations.mock import loader
from services.operations.apps.operations.schema.operations.base import (
    GetOperationResponseSchema,
    GetOperationsQuerySchema,
    GetOperationsResponseSchema,
    CreateOperationRequestSchema,
    CreateOperationResponseSchema,
    GetOperationsSummaryQuerySchema,
    GetOperationsSummaryResponseSchema,
)

operations_mock_router = APIRouter(
    prefix=APIRoutes.OPERATIONS,
    tags=[APIRoutes.OPERATIONS.as_tag()]
)


@operations_mock_router.get('', response_model=GetOperationsResponseSchema)
async def get_operations_view(query: Annotated[GetOperationsQuerySchema, Depends(GetOperationsQuerySchema.as_query)]):
    return await loader.load_http_with_timeout("get_operations/default.json", GetOperationsResponseSchema)


@operations_mock_router.get(
    '/operations-summary',
    response_model=GetOperationsSummaryResponseSchema
)
async def get_operations_summary_view(
        query: Annotated[GetOperationsSummaryQuerySchema, Depends(GetOperationsSummaryQuerySchema.as_query)],
):
    return await loader.load_http_with_timeout(
        "get_operations_summary/default.json", GetOperationsSummaryResponseSchema
    )


@operations_mock_router.get('/{operation_id}', response_model=GetOperationResponseSchema)
async def get_operation_view(operation_id: uuid.UUID):
    return await loader.load_http_with_timeout("get_operation/default.json", GetOperationResponseSchema)


@operations_mock_router.post('', response_model=CreateOperationResponseSchema)
async def create_operation_view(request: CreateOperationRequestSchema):
    return await loader.load_http_with_timeout("create_operation/default.json", CreateOperationResponseSchema)
