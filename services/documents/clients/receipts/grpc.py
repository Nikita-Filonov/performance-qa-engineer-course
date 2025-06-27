from config import settings
from contracts.services.documents.receipts.receipt_pb2 import Receipt
from contracts.services.documents.receipts.receipts_service_pb2_grpc import ReceiptsServiceStub
from contracts.services.documents.receipts.rpc_create_receipt_pb2 import CreateReceiptRequest, CreateReceiptResponse
from contracts.services.documents.receipts.rpc_get_receipt_pb2 import GetReceiptRequest, GetReceiptResponse
from libs.grpc.client.base import GRPCClient
from libs.logger import get_logger


class ReceiptsGRPCClient(GRPCClient):
    stub: ReceiptsServiceStub
    stub_class = ReceiptsServiceStub

    async def get_receipt_api(self, request: GetReceiptRequest) -> GetReceiptResponse:
        return await self.stub.GetReceipt(request)

    async def create_receipt_api(self, request: CreateReceiptRequest) -> CreateReceiptResponse:
        return await self.stub.CreateReceipt(request)

    async def get_receipt(self, operation_id: str) -> Receipt:
        request = GetReceiptRequest(operation_id=operation_id)
        response = await self.get_receipt_api(request)
        return response.receipt

    async def create_receipt(self, operation_id: str, content: bytes) -> Receipt:
        request = CreateReceiptRequest(operation_id=operation_id, content=content)
        response = await self.create_receipt_api(request)
        return response.receipt


def get_receipts_grpc_client() -> ReceiptsGRPCClient:
    logger = get_logger("RECEIPTS_SERVICE_GRPC_CLIENT")
    return ReceiptsGRPCClient(config=settings.documents_grpc_client, logger=logger)
