from contracts.services.gateway.operations.rpc_get_operation_pb2 import (
    GetOperationRequest,
    GetOperationResponse
)
from contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import (
    GetOperationReceiptRequest,
    GetOperationReceiptResponse
)
from contracts.services.gateway.operations.rpc_get_operations_pb2 import (
    GetOperationsRequest,
    GetOperationsResponse
)
from contracts.services.gateway.operations.rpc_get_operations_summary_pb2 import (
    GetOperationsSummaryRequest,
    GetOperationsSummaryResponse
)
from contracts.services.gateway.operations.rpc_make_bill_payment_operation_pb2 import (
    MakeBillPaymentOperationRequest,
    MakeBillPaymentOperationResponse
)
from contracts.services.gateway.operations.rpc_make_cash_withdrawal_operation_pb2 import (
    MakeCashWithdrawalOperationRequest,
    MakeCashWithdrawalOperationResponse
)
from contracts.services.gateway.operations.rpc_make_cashback_operation_pb2 import (
    MakeCashbackOperationRequest,
    MakeCashbackOperationResponse
)
from contracts.services.gateway.operations.rpc_make_fee_operation_pb2 import (
    MakeFeeOperationRequest,
    MakeFeeOperationResponse
)
from contracts.services.gateway.operations.rpc_make_purchase_operation_pb2 import (
    MakePurchaseOperationRequest,
    MakePurchaseOperationResponse
)
from contracts.services.gateway.operations.rpc_make_top_up_operation_pb2 import (
    MakeTopUpOperationRequest,
    MakeTopUpOperationResponse
)
from contracts.services.gateway.operations.rpc_make_transfer_operation_pb2 import (
    MakeTransferOperationRequest,
    MakeTransferOperationResponse
)
from services.operations.clients.operations.grpc import OperationsGRPCClient


async def get_operation(
        request: GetOperationRequest,
        operations_grpc_client: OperationsGRPCClient
) -> GetOperationResponse:
    operation = await operations_grpc_client.get_operation(request.id)

    return GetOperationResponse(operation=operation)


async def get_operations(
        request: GetOperationsRequest,
        operations_grpc_client: OperationsGRPCClient
) -> GetOperationsResponse:
    operations = await operations_grpc_client.get_operations(request.account_id)

    return GetOperationsResponse(operations=operations)


async def get_operation_receipt(
        request: GetOperationReceiptRequest,
        operations_grpc_client: OperationsGRPCClient
) -> GetOperationReceiptResponse:
    receipt = await operations_grpc_client.get_operation_receipt(request.operation_id)

    return GetOperationReceiptResponse(receipt=receipt)


async def get_operations_summary(
        request: GetOperationsSummaryRequest,
        operations_grpc_client: OperationsGRPCClient
) -> GetOperationsSummaryResponse:
    summary = await operations_grpc_client.get_operations_summary(request.account_id)

    return GetOperationsSummaryResponse(summary=summary)


async def make_fee_operation(
        request: MakeFeeOperationRequest,
        operations_grpc_client: OperationsGRPCClient
) -> MakeFeeOperationResponse:
    operation = await operations_grpc_client.make_fee_operation(
        status=request.status,
        amount=request.amount,
        card_id=request.card_id,
        account_id=request.account_id
    )

    return MakeFeeOperationResponse(operation=operation)


async def make_top_up_operation(
        request: MakeTopUpOperationRequest,
        operations_grpc_client: OperationsGRPCClient
) -> MakeTopUpOperationResponse:
    operation = await operations_grpc_client.make_top_up_operation(
        status=request.status,
        amount=request.amount,
        card_id=request.card_id,
        account_id=request.account_id
    )

    return MakeTopUpOperationResponse(operation=operation)


async def make_purchase_operation(
        request: MakePurchaseOperationRequest,
        operations_grpc_client: OperationsGRPCClient
) -> MakePurchaseOperationResponse:
    operation = await operations_grpc_client.make_purchase_operation(
        status=request.status,
        amount=request.amount,
        card_id=request.card_id,
        category=request.category,
        account_id=request.account_id
    )

    return MakeTopUpOperationResponse(operation=operation)


async def make_cashback_operation(
        request: MakeCashbackOperationRequest,
        operations_grpc_client: OperationsGRPCClient
) -> MakeCashbackOperationResponse:
    operation = await operations_grpc_client.make_cashback_operation(
        status=request.status,
        amount=request.amount,
        card_id=request.card_id,
        account_id=request.account_id
    )

    return MakeCashbackOperationResponse(operation=operation)


async def make_transfer_operation(
        request: MakeTransferOperationRequest,
        operations_grpc_client: OperationsGRPCClient
) -> MakeTransferOperationResponse:
    operation = await operations_grpc_client.make_transfer_operation(
        status=request.status,
        amount=request.amount,
        card_id=request.card_id,
        account_id=request.account_id
    )

    return MakeTransferOperationResponse(operation=operation)


async def make_bill_payment_operation(
        request: MakeBillPaymentOperationRequest,
        operations_grpc_client: OperationsGRPCClient
) -> MakeBillPaymentOperationResponse:
    operation = await operations_grpc_client.make_bill_payment_operation(
        status=request.status,
        amount=request.amount,
        card_id=request.card_id,
        account_id=request.account_id
    )

    return MakeBillPaymentOperationResponse(operation=operation)


async def make_cash_withdrawal_operation(
        request: MakeCashWithdrawalOperationRequest,
        operations_grpc_client: OperationsGRPCClient
) -> MakeCashWithdrawalOperationResponse:
    operation = await operations_grpc_client.make_cash_withdrawal_operation(
        status=request.status,
        amount=request.amount,
        card_id=request.card_id,
        account_id=request.account_id
    )

    return MakeCashWithdrawalOperationResponse(operation=operation)
