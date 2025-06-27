import uuid

from grpc import StatusCode
from grpc.aio import ServicerContext, AioRpcError

from contracts.services.operations.operation_pb2 import (
    Operation,
    OperationType as ProtoOperationType,
    OperationStatus as ProtoOperationStatus
)
from contracts.services.operations.operations_summary_pb2 import OperationsSummary
from contracts.services.operations.rpc_create_operation_pb2 import CreateOperationRequest, CreateOperationResponse
from contracts.services.operations.rpc_get_operation_pb2 import GetOperationRequest, GetOperationResponse
from contracts.services.operations.rpc_get_operations_pb2 import GetOperationsRequest, GetOperationsResponse
from contracts.services.operations.rpc_get_operations_summary_pb2 import (
    GetOperationsSummaryRequest,
    GetOperationsSummaryResponse
)
from contracts.services.payments.payment_pb2 import PaymentStatus
from libs.base.date import from_proto_datetime, to_proto_datetime
from services.accounts.clients.accounts.grpc import AccountsGRPCClient
from services.cards.clients.cards.grpc import CardsGRPCClient
from services.documents.services.kafka.producer import DocumentsKafkaProducerClient
from services.operations.services.postgres.models.operations import OperationType, OperationStatus, OperationsModel
from services.operations.services.postgres.repositories.operations import OperationsRepository, CreateOperationDict
from services.payments.clients.payments.grpc import PaymentsGRPCClient

MAP_OPERATION_TYPE_TO_PROTO = OperationType.to_proto_map(ProtoOperationType)
MAP_OPERATION_TYPE_FROM_PROTO = OperationType.from_proto_map(ProtoOperationType)
MAP_OPERATION_STATUS_TO_PROTO = OperationStatus.to_proto_map(ProtoOperationStatus)
MAP_OPERATION_STATUS_FROM_PROTO = OperationStatus.from_proto_map(ProtoOperationStatus)


def build_operation_from_model(model: OperationsModel) -> Operation:
    return Operation(
        id=str(model.id),
        type=MAP_OPERATION_TYPE_TO_PROTO[model.type],
        status=MAP_OPERATION_STATUS_TO_PROTO[model.status],
        amount=model.amount,
        card_id=str(model.card_id),
        category=model.category,
        created_at=to_proto_datetime(model.created_at),
        account_id=str(model.account_id)
    )


async def get_operation(
        context: ServicerContext,
        request: GetOperationRequest,
        operations_repository: OperationsRepository
) -> GetOperationResponse:
    operation = await operations_repository.get_by_id(uuid.UUID(request.id))
    if not operation:
        await context.abort(
            code=StatusCode.NOT_FOUND,
            details=f"Operation with id {request.id} not found"
        )

    return GetOperationResponse(operation=build_operation_from_model(operation))


async def get_operations(
        request: GetOperationsRequest,
        operations_repository: OperationsRepository
) -> GetOperationsResponse:
    operations = await operations_repository.filter(account_id=uuid.UUID(request.account_id))

    return GetOperationsResponse(
        operations=[build_operation_from_model(operation) for operation in operations]
    )


async def create_operation(
        context: ServicerContext,
        request: CreateOperationRequest,
        cards_grpc_client: CardsGRPCClient,
        payments_grpc_client: PaymentsGRPCClient,
        accounts_grpc_client: AccountsGRPCClient,
        operations_repository: OperationsRepository,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> CreateOperationResponse:
    try:
        card = await cards_grpc_client.get_card(request.card_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Create operation: {error.details()}"
        )

    try:
        account = await accounts_grpc_client.get_account(request.account_id)
    except AioRpcError as error:
        await context.abort(
            code=error.code(),
            details=f"Create operation: {error.details()}"
        )

    payment = await payments_grpc_client.authorize_payment(
        cvv=card.cvv,
        amount=request.amount,
        expiry_date=card.expiry_date,
        card_number=card.card_number,
        card_holder=card.card_holder
    )

    if payment.status == PaymentStatus.PAYMENT_STATUS_FAILED:
        request.status = ProtoOperationStatus.OPERATION_STATUS_FAILED

    if payment.status == PaymentStatus.PAYMENT_STATUS_AUTHORIZED:
        await payments_grpc_client.capture_payment(payment.id)

    operation = await operations_repository.create(
        CreateOperationDict(
            type=MAP_OPERATION_TYPE_FROM_PROTO[request.type],
            status=MAP_OPERATION_STATUS_FROM_PROTO[request.status],
            amount=request.amount,
            card_id=uuid.UUID(card.id),
            category=request.category,
            created_at=from_proto_datetime(request.created_at),
            account_id=uuid.UUID(account.id)
        )
    )

    if OperationStatus(operation.status).is_success():
        await accounts_grpc_client.update_account_balance(
            balance=account.balance + request.amount,
            account_id=account.id
        )
        await documents_kafka_producer_client.produce_receipt_document(
            content=str(operation.id).encode(),
            operation_id=operation.id
        )

    return CreateOperationResponse(operation=build_operation_from_model(operation))


async def get_operations_summary(
        request: GetOperationsSummaryRequest,
        operations_repository: OperationsRepository
) -> GetOperationsSummaryResponse:
    summary = await operations_repository.get_operations_summary(
        account_id=uuid.UUID(request.account_id)
    )

    return GetOperationsSummaryResponse(
        summary=OperationsSummary(
            spent_amount=summary.spent_amount,
            received_amount=summary.received_amount,
            cashback_amount=summary.cashback_amount
        )
    )
