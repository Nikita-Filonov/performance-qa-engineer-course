from grpc import StatusCode
from grpc.aio import AioRpcError, ServicerContext

from contracts.services.documents.receipts.receipt_pb2 import Receipt
from contracts.services.documents.receipts.rpc_create_receipt_pb2 import CreateReceiptRequest, CreateReceiptResponse
from contracts.services.documents.receipts.rpc_get_receipt_pb2 import GetReceiptRequest, GetReceiptResponse
from libs.s3.client import S3File
from services.documents.services.s3.client import DocumentsS3Client
from services.operations.clients.operations.grpc import OperationsGRPCClient


def build_receipt_from_file(file: S3File) -> Receipt:
    return Receipt(url=file.url, document=file.content)


async def get_receipt(
        context: ServicerContext,
        request: GetReceiptRequest,
        documents_s3_client: DocumentsS3Client,
        operations_grpc_client: OperationsGRPCClient,
) -> GetReceiptResponse:
    try:
        operation = await operations_grpc_client.get_operation(request.operation_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Get receipt: {error.details()}"
        )

    try:
        file = await documents_s3_client.get_receipt_file(operation.id)
    except Exception as error:
        await context.abort(
            code=StatusCode.INTERNAL,
            details=f"Get receipt: {error}"
        )

    return GetReceiptResponse(receipt=build_receipt_from_file(file))


async def create_receipt(
        context: ServicerContext,
        request: CreateReceiptRequest,
        documents_s3_client: DocumentsS3Client,
        operations_grpc_client: OperationsGRPCClient,
) -> CreateReceiptResponse:
    try:
        account = await operations_grpc_client.get_operation(request.operation_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Create receipt: {error.details()}"
        )

    file = await documents_s3_client.upload_receipt_file(account.id, request.content)

    return CreateReceiptResponse(receipt=build_receipt_from_file(file))
