import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.documents.apps.receipts.controllers.receipts.http import get_receipt, create_receipt
from services.documents.apps.receipts.schema.receipts import (
    GetReceiptResponseSchema,
    CreateReceiptRequestSchema,
    CreateReceiptResponseSchema
)
from services.documents.services.s3.client import get_documents_s3_client, DocumentsS3Client
from services.operations.clients.operations.http import OperationsHTTPClient, get_operations_http_client

receipts_router = APIRouter(
    prefix=APIRoutes.RECEIPTS,
    tags=[APIRoutes.RECEIPTS.as_tag()]
)


@receipts_router.get('/{operation_id}', response_model=GetReceiptResponseSchema)
async def get_receipt_view(
        operation_id: uuid.UUID,
        documents_s3_client: Annotated[DocumentsS3Client, Depends(get_documents_s3_client)],
        operations_http_client: Annotated[OperationsHTTPClient, Depends(get_operations_http_client)]
):
    return await get_receipt(
        operation_id=operation_id,
        documents_s3_client=documents_s3_client,
        operations_http_client=operations_http_client
    )


@receipts_router.post('', response_model=CreateReceiptResponseSchema)
async def create_receipt_view(
        request: CreateReceiptRequestSchema,
        documents_s3_client: Annotated[DocumentsS3Client, Depends(get_documents_s3_client)],
        operations_http_client: Annotated[OperationsHTTPClient, Depends(get_operations_http_client)]
):
    return await create_receipt(
        request=request,
        documents_s3_client=documents_s3_client,
        operations_http_client=operations_http_client
    )
