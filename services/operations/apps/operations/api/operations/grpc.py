from grpc.aio import ServicerContext

from contracts.services.operations.operations_service_pb2_grpc import OperationsServiceServicer
from contracts.services.operations.rpc_create_operation_pb2 import CreateOperationRequest, CreateOperationResponse
from contracts.services.operations.rpc_get_operation_pb2 import GetOperationRequest, GetOperationResponse
from contracts.services.operations.rpc_get_operations_pb2 import GetOperationsRequest, GetOperationsResponse
from contracts.services.operations.rpc_get_operations_summary_pb2 import (
    GetOperationsSummaryRequest,
    GetOperationsSummaryResponse
)
from services.accounts.clients.accounts.grpc import get_accounts_grpc_client
from services.cards.clients.cards.grpc import get_cards_grpc_client
from services.documents.services.kafka.producer import get_documents_kafka_producer_client
from services.operations.apps.operations.controllers.operations.grpc import (
    get_operation,
    get_operations,
    create_operation,
    get_operations_summary
)
from services.operations.services.postgres.repositories.operations import get_operations_repository_context
from services.payments.clients.payments.grpc import get_payments_grpc_client


class OperationsService(OperationsServiceServicer):
    async def GetOperation(self, request: GetOperationRequest, context: ServicerContext) -> GetOperationResponse:
        async with get_operations_repository_context() as operations_repository:
            return await get_operation(context, request, operations_repository)

    async def GetOperations(self, request: GetOperationsRequest, context: ServicerContext) -> GetOperationsResponse:
        async with get_operations_repository_context() as operations_repository:
            return await get_operations(request, operations_repository)

    async def CreateOperation(
            self,
            request: CreateOperationRequest,
            context: ServicerContext
    ) -> CreateOperationResponse:
        async with get_operations_repository_context() as operations_repository:
            return await create_operation(
                context=context,
                request=request,
                cards_grpc_client=get_cards_grpc_client(),
                payments_grpc_client=get_payments_grpc_client(),
                accounts_grpc_client=get_accounts_grpc_client(),
                operations_repository=operations_repository,
                documents_kafka_producer_client=get_documents_kafka_producer_client()
            )

    async def GetOperationsSummary(
            self,
            request: GetOperationsSummaryRequest,
            context: ServicerContext
    ) -> GetOperationsSummaryResponse:
        async with get_operations_repository_context() as operations_repository:
            return await get_operations_summary(
                request=request,
                operations_repository=operations_repository
            )
