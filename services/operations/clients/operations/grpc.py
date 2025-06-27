from datetime import datetime

from config import settings
from contracts.services.operations.operation_pb2 import Operation, OperationType, OperationStatus
from contracts.services.operations.operations_service_pb2_grpc import OperationsServiceStub
from contracts.services.operations.operations_summary_pb2 import OperationsSummary
from contracts.services.operations.rpc_create_operation_pb2 import CreateOperationRequest, CreateOperationResponse
from contracts.services.operations.rpc_get_operation_pb2 import GetOperationRequest, GetOperationResponse
from contracts.services.operations.rpc_get_operations_pb2 import GetOperationsRequest, GetOperationsResponse
from contracts.services.operations.rpc_get_operations_summary_pb2 import (
    GetOperationsSummaryRequest,
    GetOperationsSummaryResponse
)
from libs.base.date import to_proto_datetime
from libs.grpc.client.base import GRPCClient
from libs.logger import get_logger
from services.operations.clients.operations.base import positive_amount, negative_amount, Category


class OperationsGRPCClient(GRPCClient):
    stub: OperationsServiceStub
    stub_class = OperationsServiceStub

    async def get_operation_api(self, request: GetOperationRequest) -> GetOperationResponse:
        return await self.stub.GetOperation(request)

    async def get_operations_api(self, request: GetOperationsRequest) -> GetOperationsResponse:
        return await self.stub.GetOperations(request)

    async def create_operation_api(self, request: CreateOperationRequest) -> CreateOperationResponse:
        return await self.stub.CreateOperation(request)

    async def get_operations_summary_api(self, request: GetOperationsSummaryRequest) -> GetOperationsSummaryResponse:
        return await self.stub.GetOperationsSummary(request)

    async def get_operation(self, operation_id: str) -> Operation:
        request = GetOperationRequest(id=operation_id)
        response = await self.get_operation_api(request)
        return response.operation

    async def get_operations(self, account_id: str) -> list[Operation]:
        request = GetOperationsRequest(account_id=account_id)
        response = await self.get_operations_api(request)
        return response.operations

    async def make_fee_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> Operation:
        request = CreateOperationRequest(
            type=OperationType.OPERATION_TYPE_FEE,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=Category.FEE,
            created_at=to_proto_datetime(datetime.now()),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return response.operation

    async def make_top_up_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> Operation:
        request = CreateOperationRequest(
            type=OperationType.OPERATION_TYPE_TOP_UP,
            status=status,
            amount=positive_amount(amount),
            card_id=card_id,
            category=Category.MONEY_IN,
            created_at=to_proto_datetime(datetime.now()),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return response.operation

    async def make_purchase_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            category: str,
            account_id: str
    ) -> Operation:
        request = CreateOperationRequest(
            type=OperationType.OPERATION_TYPE_PURCHASE,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=category,
            created_at=to_proto_datetime(datetime.now()),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return response.operation

    async def make_cashback_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> Operation:
        request = CreateOperationRequest(
            type=OperationType.OPERATION_TYPE_CASHBACK,
            status=status,
            amount=positive_amount(amount),
            card_id=card_id,
            category=Category.CASHBACK_REWARDS,
            created_at=to_proto_datetime(datetime.now()),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return response.operation

    async def make_transfer_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> Operation:
        request = CreateOperationRequest(
            type=OperationType.OPERATION_TYPE_TRANSFER,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=Category.TRANSFER,
            created_at=to_proto_datetime(datetime.now()),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return response.operation

    async def make_bill_payment_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> Operation:
        request = CreateOperationRequest(
            type=OperationType.OPERATION_TYPE_BILL_PAYMENT,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=Category.BILL_PAYMENT,
            created_at=to_proto_datetime(datetime.now()),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return response.operation

    async def make_cash_withdrawal_operation(
            self,
            status: OperationStatus,
            amount: float,
            card_id: str,
            account_id: str
    ) -> Operation:
        request = CreateOperationRequest(
            type=OperationType.OPERATION_TYPE_CASH_WITHDRAWAL,
            status=status,
            amount=negative_amount(amount),
            card_id=card_id,
            category=Category.CASH_WITHDRAWAL,
            created_at=to_proto_datetime(datetime.now()),
            account_id=account_id,
        )
        response = await self.create_operation_api(request)
        return response.operation

    async def get_operations_summary(self, account_id: str) -> OperationsSummary:
        request = GetOperationsSummaryRequest(account_id=account_id)
        response = await self.get_operations_summary_api(request)
        return response.summary


def get_operations_grpc_client() -> OperationsGRPCClient:
    logger = get_logger("OPERATIONS_SERVICE_GRPC_CLIENT")
    return OperationsGRPCClient(config=settings.operations_grpc_client, logger=logger)
