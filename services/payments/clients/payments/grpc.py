import uuid

from config import settings
from contracts.services.payments.payment_pb2 import Payment, PaymentSystem, PaymentStatus
from contracts.services.payments.payments_service_pb2_grpc import PaymentsServiceStub
from contracts.services.payments.rpc_authorize_payment_pb2 import (
    AuthorizePaymentRequest,
    AuthorizePaymentResponse
)
from contracts.services.payments.rpc_capture_payment_pb2 import (
    CapturePaymentRequest,
    CapturePaymentResponse
)
from contracts.services.payments.rpc_refund_payment_pb2 import (
    RefundPaymentRequest,
    RefundPaymentResponse
)
from libs.grpc.client.base import GRPCClient
from libs.logger import get_logger


def build_authorized_payment() -> Payment:
    return Payment(
        id=str(uuid.uuid4()),
        status=PaymentStatus.PAYMENT_STATUS_AUTHORIZED,
        system=PaymentSystem.PAYMENT_SYSTEM_MASTERCARD,
        message="success"
    )


class PaymentsGRPCClient(GRPCClient):
    stub: PaymentsServiceStub
    stub_class = PaymentsServiceStub

    async def refund_payment_api(self, request: RefundPaymentRequest) -> RefundPaymentResponse:
        return await self.stub.RefundPayment(request)

    async def capture_payment_api(self, request: CapturePaymentRequest) -> CapturePaymentResponse:
        return await self.stub.CapturePayment(request)

    async def authorize_payment_api(self, request: AuthorizePaymentRequest) -> AuthorizePaymentResponse:
        return await self.stub.AuthorizePayment(request)

    async def refund_payment(self, amount: float, payment_id: str) -> Payment:
        if not settings.payments_system_enabled:
            return build_authorized_payment()

        request = RefundPaymentRequest(
            amount=amount,
            system=PaymentSystem.PAYMENT_SYSTEM_MASTERCARD,
            payment_id=payment_id
        )
        response = await self.refund_payment_api(request)
        return response.payment

    async def capture_payment(self, payment_id: str) -> Payment:
        if not settings.payments_system_enabled:
            return build_authorized_payment()

        request = CapturePaymentRequest(
            system=PaymentSystem.PAYMENT_SYSTEM_MASTERCARD,
            payment_id=payment_id
        )
        response = await self.capture_payment_api(request)
        return response.payment

    async def authorize_payment(
            self,
            cvv: str,
            amount: float,
            expiry_date: str,
            card_number: str,
            card_holder: str,
    ) -> Payment:
        if not settings.payments_system_enabled:
            return build_authorized_payment()

        request = AuthorizePaymentRequest(
            cvv=cvv,
            amount=amount,
            system=PaymentSystem.PAYMENT_SYSTEM_MASTERCARD,
            expiry_date=expiry_date,
            card_number=card_number,
            card_holder=card_holder
        )
        response = await self.authorize_payment_api(request)
        return response.payment


def get_payments_grpc_client() -> PaymentsGRPCClient:
    logger = get_logger("PAYMENTS_SERVICE_GRPC_CLIENT")
    return PaymentsGRPCClient(config=settings.payments_grpc_client, logger=logger)
