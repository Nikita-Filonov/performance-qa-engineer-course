from grpc.aio import ServicerContext

from contracts.services.documents.receipts.receipts_service_pb2_grpc import ReceiptsServiceServicer
from contracts.services.documents.receipts.rpc_create_receipt_pb2 import CreateReceiptRequest, CreateReceiptResponse
from contracts.services.documents.receipts.rpc_get_receipt_pb2 import GetReceiptRequest, GetReceiptResponse
from services.mock.apps.documents.receipts.mock import loader


class ReceiptsMockService(ReceiptsServiceServicer):
    async def GetReceipt(self, request: GetReceiptRequest, context: ServicerContext) -> GetReceiptResponse:
        return loader.load_grpc('GetReceipt/default.json', GetReceiptResponse)

    async def CreateReceipt(self, request: CreateReceiptRequest, context: ServicerContext) -> CreateReceiptResponse:
        return loader.load_grpc('CreateReceipt/default.json', CreateReceiptResponse)
