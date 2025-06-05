import uuid
from datetime import date

from httpx import Response

from config import settings
from libs.http.client.base import HTTPClient
from libs.http.client.handlers import handle_http_error, HTTPClientError
from libs.logger import get_logger
from libs.routes import APIRoutes
from services.payments.apps.payments.schema.payments import (
    PaymentSystem,
    PaymentStatus,
    PaymentSchema,
    RefundPaymentRequestSchema,
    RefundPaymentResponseSchema,
    CapturePaymentRequestSchema,
    CapturePaymentResponseSchema,
    AuthorizePaymentRequestSchema,
    AuthorizePaymentResponseSchema
)


def build_authorized_payment() -> PaymentSchema:
    return PaymentSchema(
        id=uuid.uuid4(),
        status=PaymentStatus.AUTHORIZED,
        system=PaymentSystem.MASTERCARD,
        message="success"
    )


class PaymentsHTTPClientError(HTTPClientError):
    pass


class PaymentsHTTPClient(HTTPClient):
    @handle_http_error(client='PaymentsHTTPClient', exception=PaymentsHTTPClientError)
    async def refund_payment_api(self, request: RefundPaymentRequestSchema) -> Response:
        return await self.post(
            f'{APIRoutes.PAYMENTS}/refund-payment',
            json=request.model_dump(mode='json', by_alias=True)
        )

    @handle_http_error(client='PaymentsHTTPClient', exception=PaymentsHTTPClientError)
    async def capture_payment_api(self, request: CapturePaymentRequestSchema) -> Response:
        return await self.post(
            f'{APIRoutes.PAYMENTS}/capture-payment',
            json=request.model_dump(mode='json', by_alias=True)
        )

    @handle_http_error(client='PaymentsHTTPClient', exception=PaymentsHTTPClientError)
    async def authorize_payment_api(self, request: AuthorizePaymentRequestSchema) -> Response:
        return await self.post(
            f'{APIRoutes.PAYMENTS}/authorize-payment',
            json=request.model_dump(mode='json', by_alias=True)
        )

    async def refund_payment(
            self,
            amount: float,
            payment_id: uuid.UUID
    ) -> RefundPaymentResponseSchema:
        if not settings.payments_system_enabled:
            return RefundPaymentResponseSchema(payment=build_authorized_payment())

        request = RefundPaymentRequestSchema(
            amount=amount,
            system=PaymentSystem.MASTERCARD,
            payment_id=payment_id
        )
        response = await self.refund_payment_api(request)
        return RefundPaymentResponseSchema.model_validate_json(response.text)

    async def capture_payment(self, payment_id: uuid.UUID) -> CapturePaymentResponseSchema:
        if not settings.payments_system_enabled:
            return CapturePaymentResponseSchema(payment=build_authorized_payment())

        request = CapturePaymentRequestSchema(
            system=PaymentSystem.MASTERCARD,
            payment_id=payment_id
        )
        response = await self.capture_payment_api(request)
        return CapturePaymentResponseSchema.model_validate_json(response.text)

    async def authorize_payment(
            self,
            cvv: str,
            amount: float,
            expiry_date: date,
            card_number: str,
            card_holder: str,
    ) -> AuthorizePaymentResponseSchema:
        if not settings.payments_system_enabled:
            return AuthorizePaymentResponseSchema(payment=build_authorized_payment())

        request = AuthorizePaymentRequestSchema(
            cvv=cvv,
            amount=amount,
            system=PaymentSystem.MASTERCARD,
            expiry_date=expiry_date,
            card_number=card_number,
            card_holder=card_holder
        )
        response = await self.authorize_payment_api(request)
        return AuthorizePaymentResponseSchema.model_validate_json(response.text)


def get_payments_http_client() -> PaymentsHTTPClient:
    logger = get_logger("PAYMENTS_SERVICE_HTTP_CLIENT")
    return PaymentsHTTPClient(config=settings.payments_http_client, logger=logger)
