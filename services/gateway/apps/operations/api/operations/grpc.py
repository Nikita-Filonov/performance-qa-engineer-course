from grpc.aio import ServicerContext

from contracts.services.gateway.operations.operations_gateway_service_pb2_grpc import OperationsGatewayServiceServicer
from contracts.services.gateway.operations.rpc_get_operation_pb2 import (
    GetOperationRequest,
    GetOperationResponse
)
from contracts.services.gateway.operations.rpc_get_operation_receipt_pb2 import (
    GetOperationReceiptRequest
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
from services.documents.clients.receipts.grpc import get_receipts_grpc_client
from services.gateway.apps.operations.controllers.operations.grpc import make_fee_operation, make_top_up_operation, \
    make_cashback_operation, make_purchase_operation, make_transfer_operation, make_bill_payment_operation, \
    make_cash_withdrawal_operation, get_operation, get_operations, get_operations_summary, get_operation_receipt
from services.operations.clients.operations.grpc import get_operations_grpc_client


class OperationsGatewayService(OperationsGatewayServiceServicer):
    async def GetOperation(
            self,
            request: GetOperationRequest,
            context: ServicerContext
    ) -> GetOperationResponse:
        return await get_operation(
            request=request,
            operations_grpc_client=get_operations_grpc_client()
        )

    async def GetOperations(
            self,
            request: GetOperationsRequest,
            context: ServicerContext
    ) -> GetOperationsResponse:
        return await get_operations(
            request=request,
            operations_grpc_client=get_operations_grpc_client()
        )

    async def GetOperationReceipt(
            self,
            request: GetOperationReceiptRequest,
            context: ServicerContext
    ):
        return await get_operation_receipt(
            request=request,
            receipts_grpc_client=get_receipts_grpc_client()
        )

    async def GetOperationsSummary(
            self,
            request: GetOperationsSummaryRequest,
            context: ServicerContext
    ) -> GetOperationsSummaryResponse:
        return await get_operations_summary(
            request=request,
            operations_grpc_client=get_operations_grpc_client()
        )

    async def MakeFeeOperation(
            self,
            request: MakeFeeOperationRequest,
            context: ServicerContext
    ) -> MakeFeeOperationResponse:
        return await make_fee_operation(
            request=request,
            operations_grpc_client=get_operations_grpc_client(),
        )

    async def MakeTopUpOperation(
            self,
            request: MakeTopUpOperationRequest,
            context: ServicerContext
    ) -> MakeTopUpOperationResponse:
        return await make_top_up_operation(
            request=request,
            operations_grpc_client=get_operations_grpc_client(),
        )

    async def MakeCashbackOperation(
            self,
            request: MakeCashbackOperationRequest,
            context: ServicerContext
    ) -> MakeCashbackOperationResponse:
        return await make_cashback_operation(
            request=request,
            operations_grpc_client=get_operations_grpc_client(),
        )

    async def MakePurchaseOperation(
            self,
            request: MakePurchaseOperationRequest,
            context: ServicerContext
    ) -> MakePurchaseOperationResponse:
        return await make_purchase_operation(
            request=request,
            operations_grpc_client=get_operations_grpc_client(),
        )

    async def MakeTransferOperation(
            self,
            request: MakeTransferOperationRequest,
            context: ServicerContext
    ) -> MakeTransferOperationResponse:
        return await make_transfer_operation(
            request=request,
            operations_grpc_client=get_operations_grpc_client()
        )

    async def MakeBillPaymentOperation(
            self,
            request: MakeBillPaymentOperationRequest,
            context: ServicerContext
    ) -> MakeBillPaymentOperationResponse:
        return await make_bill_payment_operation(
            request=request,
            operations_grpc_client=get_operations_grpc_client()
        )

    async def MakeCashWithdrawalOperation(
            self,
            request: MakeCashWithdrawalOperationRequest,
            context: ServicerContext
    ) -> MakeCashWithdrawalOperationResponse:
        return await make_cash_withdrawal_operation(
            request=request,
            operations_grpc_client=get_operations_grpc_client()
        )
