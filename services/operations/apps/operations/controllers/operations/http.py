import uuid

from fastapi import HTTPException, status

from services.accounts.clients.accounts.http import AccountsHTTPClient, AccountsHTTPClientError
from services.cards.clients.cards.http import CardsHTTPClient, CardsHTTPClientError
from services.documents.services.kafka.producer import DocumentsKafkaProducerClient
from services.operations.apps.operations.schema.operations.base import (
    GetOperationResponseSchema,
    GetOperationsQuerySchema,
    GetOperationsResponseSchema,
    CreateOperationRequestSchema,
    CreateOperationResponseSchema,
    GetOperationsSummaryQuerySchema,
    GetOperationsSummaryResponseSchema,
)
from services.operations.apps.operations.schema.operations.operation import OperationSchema
from services.operations.apps.operations.schema.operations.operations_summary import OperationsSummarySchema
from services.operations.services.postgres.models.operations import OperationStatus
from services.operations.services.postgres.repositories.operations import OperationsRepository, CreateOperationDict
from services.payments.apps.payments.schema.payments import PaymentStatus
from services.payments.clients.payments.http import PaymentsHTTPClient


async def get_operation(
        operation_id: uuid.UUID,
        operations_repository: OperationsRepository
) -> GetOperationResponseSchema:
    operation = await operations_repository.get_by_id(operation_id)
    if not operation:
        raise HTTPException(
            detail=f"Operation with id {operation_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return GetOperationResponseSchema(operation=OperationSchema.model_validate(operation))


async def get_operations(
        query: GetOperationsQuerySchema,
        operations_repository: OperationsRepository
) -> GetOperationsResponseSchema:
    operations = await operations_repository.filter(account_id=query.account_id)

    return GetOperationsResponseSchema(
        operations=[OperationSchema.model_validate(operation) for operation in operations]
    )


async def create_operation(
        request: CreateOperationRequestSchema,
        cards_http_client: CardsHTTPClient,
        payments_http_client: PaymentsHTTPClient,
        accounts_http_client: AccountsHTTPClient,
        operations_repository: OperationsRepository,
        documents_kafka_producer_client: DocumentsKafkaProducerClient
) -> CreateOperationResponseSchema:
    try:
        get_card_response = await cards_http_client.get_card(request.card_id)
    except CardsHTTPClientError as error:
        raise HTTPException(
            detail=f"Create operation: {error.details}",
            status_code=error.status_code
        )

    try:
        get_account_response = await accounts_http_client.get_account(request.account_id)
    except AccountsHTTPClientError as error:
        raise HTTPException(
            detail=f"Create operation: {error.details}",
            status_code=error.status_code
        )

    authorize_payment_response = await payments_http_client.authorize_payment(
        cvv=get_card_response.card.cvv,
        amount=request.amount,
        expiry_date=get_card_response.card.expiry_date,
        card_number=get_card_response.card.card_number,
        card_holder=get_card_response.card.card_holder
    )

    if authorize_payment_response.payment.status == PaymentStatus.FAILED:
        request.status = OperationStatus.FAILED

    if authorize_payment_response.payment.status == PaymentStatus.AUTHORIZED:
        await payments_http_client.capture_payment(authorize_payment_response.payment.id)

    operation = await operations_repository.create(
        CreateOperationDict(
            type=request.type,
            status=request.status,
            amount=request.amount,
            card_id=get_card_response.card.id,
            category=request.category,
            created_at=request.created_at,
            account_id=get_account_response.account.id
        )
    )

    if OperationStatus(operation.status).is_success():
        await accounts_http_client.update_account_balance(
            balance=get_account_response.account.balance + request.amount,
            account_id=get_account_response.account.id
        )
        await documents_kafka_producer_client.produce_receipt_document(
            content=str(operation.id).encode(),
            operation_id=operation.id
        )

    return CreateOperationResponseSchema(operation=OperationSchema.model_validate(operation))


async def get_operations_summary(
        query: GetOperationsSummaryQuerySchema,
        operations_repository: OperationsRepository
) -> GetOperationsSummaryResponseSchema:
    summary = await operations_repository.get_operations_summary(account_id=query.account_id)

    return GetOperationsSummaryResponseSchema(
        summary=OperationsSummarySchema.model_validate(summary)
    )
