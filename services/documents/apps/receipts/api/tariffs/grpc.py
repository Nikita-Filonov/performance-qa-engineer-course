from grpc.aio import ServicerContext

from contracts.services.documents.receipts.receipts_service_pb2_grpc import ReceiptsServiceServicer
from contracts.services.documents.receipts.rpc_create_receipt_pb2 import CreateReceiptRequest, CreateReceiptResponse
from contracts.services.documents.receipts.rpc_get_receipt_pb2 import GetReceiptRequest, GetReceiptResponse
from services.documents.apps.receipts.controllers.receipts.grpc import get_receipt, create_receipt
from services.documents.services.s3.client import get_documents_s3_client
from services.operations.clients.operations.grpc import get_operations_grpc_client


class ReceiptsService(ReceiptsServiceServicer):
    async def GetReceipt(self, request: GetReceiptRequest, context: ServicerContext) -> GetReceiptResponse:
        return await get_receipt(
            context=context,
            request=request,
            documents_s3_client=get_documents_s3_client(),
            operations_grpc_client=get_operations_grpc_client()
        )

    async def CreateReceipt(self, request: CreateReceiptRequest, context: ServicerContext) -> CreateReceiptResponse:
        return await create_receipt(
            context=context,
            request=request,
            documents_s3_client=get_documents_s3_client(),
            operations_grpc_client=get_operations_grpc_client()
        )
