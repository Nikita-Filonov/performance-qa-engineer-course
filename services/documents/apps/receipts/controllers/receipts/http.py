import uuid

from fastapi import HTTPException, status
from pydantic import HttpUrl

from libs.s3.client import S3File
from services.documents.apps.receipts.schema.receipts import (
    ReceiptSchema,
    GetReceiptResponseSchema,
    CreateReceiptRequestSchema,
    CreateReceiptResponseSchema
)
from services.documents.services.s3.client import DocumentsS3Client
from services.operations.clients.operations.http import OperationsHTTPClient, OperationsHTTPClientError


def build_receipt_from_file(file: S3File) -> ReceiptSchema:
    return ReceiptSchema(url=HttpUrl(file.url), document=file.content)


async def get_receipt(
        operation_id: uuid.UUID,
        documents_s3_client: DocumentsS3Client,
        operations_http_client: OperationsHTTPClient,
) -> GetReceiptResponseSchema:
    try:
        get_operation_response = await operations_http_client.get_operation(operation_id)
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Get receipt: {error.details}",
            status_code=error.status_code
        )

    try:
        file = await documents_s3_client.get_receipt_file(get_operation_response.operation.id)
    except Exception as error:
        raise HTTPException(
            detail=f"Get receipt: {error}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return GetReceiptResponseSchema(receipt=build_receipt_from_file(file))


async def create_receipt(
        request: CreateReceiptRequestSchema,
        documents_s3_client: DocumentsS3Client,
        operations_http_client: OperationsHTTPClient,
) -> CreateReceiptResponseSchema:
    try:
        get_operation_response = await operations_http_client.get_operation(request.operation_id)
    except OperationsHTTPClientError as error:
        raise HTTPException(
            detail=f"Create receipt: {error.details}",
            status_code=error.status_code
        )

    file = await documents_s3_client.upload_receipt_file(
        get_operation_response.operation.id, request.content
    )

    return CreateReceiptResponseSchema(receipt=build_receipt_from_file(file))
