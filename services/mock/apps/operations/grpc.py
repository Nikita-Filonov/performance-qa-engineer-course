from grpc.aio import ServicerContext

from contracts.services.operations.operations_service_pb2_grpc import OperationsServiceServicer
from contracts.services.operations.rpc_create_operation_pb2 import CreateOperationRequest, CreateOperationResponse
from contracts.services.operations.rpc_get_operation_pb2 import GetOperationRequest, GetOperationResponse
from contracts.services.operations.rpc_get_operations_pb2 import GetOperationsRequest, GetOperationsResponse
from contracts.services.operations.rpc_get_operations_summary_pb2 import (
    GetOperationsSummaryRequest,
    GetOperationsSummaryResponse
)
from services.mock.apps.operations.mock import loader


class OperationsMockService(OperationsServiceServicer):
    async def GetOperation(self, request: GetOperationRequest, context: ServicerContext) -> GetOperationResponse:
        return loader.load_grpc("GetOperation/default.json", GetOperationResponse)

    async def GetOperations(self, request: GetOperationsRequest, context: ServicerContext) -> GetOperationsResponse:
        return loader.load_grpc("GetOperations/default.json", GetOperationsResponse)

    async def CreateOperation(
            self,
            request: CreateOperationRequest,
            context: ServicerContext
    ) -> CreateOperationResponse:
        return loader.load_grpc("CreateOperation/default.json", CreateOperationResponse)

    async def GetOperationsSummary(
            self,
            request: GetOperationsSummaryRequest,
            context: ServicerContext
    ) -> GetOperationsSummaryResponse:
        return loader.load_grpc("GetOperationsSummary/default.json", GetOperationsSummaryResponse)
