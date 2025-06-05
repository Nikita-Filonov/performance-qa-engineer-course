import uuid

from httpx import Response, QueryParams

from config import settings
from libs.faker import fake
from libs.http.client.base import HTTPClient
from libs.http.client.handlers import handle_http_error, HTTPClientError
from libs.logger import get_logger
from libs.routes import APIRoutes
from services.cards.apps.cards.schema.cards import (
    GetCardResponseSchema,
    GetCardsQuerySchema,
    GetCardsResponseSchema,
    CreateCardRequestSchema,
    CreateCardResponseSchema
)
from services.cards.clients.cards.base import build_card_expired_at, build_card_holder
from services.cards.services.postgres.models.cards import CardType, CardStatus, CardPaymentSystem


class CardsHTTPClientError(HTTPClientError):
    pass


class CardsHTTPClient(HTTPClient):
    @handle_http_error(client='CardsHTTPClient', exception=CardsHTTPClientError)
    async def get_card_api(self, card_id: uuid.UUID) -> Response:
        return await self.get(f'{APIRoutes.CARDS}/{card_id}')

    @handle_http_error(client='CardsHTTPClient', exception=CardsHTTPClientError)
    async def get_cards_api(self, query: GetCardsQuerySchema) -> Response:
        return await self.get(
            APIRoutes.CARDS,
            params=QueryParams(**query.model_dump(mode='json', by_alias=True))
        )

    @handle_http_error(client='CardsHTTPClient', exception=CardsHTTPClientError)
    async def create_card_api(self, request: CreateCardRequestSchema) -> Response:
        return await self.post(
            APIRoutes.CARDS, json=request.model_dump(mode='json', by_alias=True)
        )

    async def get_card(self, card_id: uuid.UUID) -> GetCardResponseSchema:
        response = await self.get_card_api(card_id)
        return GetCardResponseSchema.model_validate_json(response.text)

    async def get_cards(self, account_id: uuid.UUID) -> GetCardsResponseSchema:
        query = GetCardsQuerySchema(account_id=account_id)
        response = await self.get_cards_api(query)
        return GetCardsResponseSchema.model_validate_json(response.text)

    async def create_virtual_card(
            self,
            first_name: str,
            last_name: str,
            account_id: uuid.UUID
    ) -> CreateCardResponseSchema:
        request = CreateCardRequestSchema(
            pin=fake.card_pin(),
            cvv=fake.card_cvv(),
            type=CardType.VIRTUAL,
            status=CardStatus.ACTIVE,
            account_id=account_id,
            card_number=fake.card_number(),
            card_holder=build_card_holder(first_name=first_name, last_name=last_name),
            expiry_date=build_card_expired_at(),
            payment_system=CardPaymentSystem.MASTERCARD
        )
        response = await self.create_card_api(request)
        return CreateCardResponseSchema.model_validate_json(response.text)

    async def create_physical_card(
            self,
            first_name: str,
            last_name: str,
            account_id: uuid.UUID
    ) -> CreateCardResponseSchema:
        request = CreateCardRequestSchema(
            pin=fake.card_pin(),
            cvv=fake.card_cvv(),
            type=CardType.PHYSICAL,
            status=CardStatus.ACTIVE,
            account_id=account_id,
            card_number=fake.card_number(),
            card_holder=build_card_holder(first_name=first_name, last_name=last_name),
            expiry_date=build_card_expired_at(),
            payment_system=CardPaymentSystem.MASTERCARD
        )
        response = await self.create_card_api(request)
        return CreateCardResponseSchema.model_validate_json(response.text)


def get_cards_http_client() -> CardsHTTPClient:
    logger = get_logger("CARDS_SERVICE_HTTP_CLIENT")
    return CardsHTTPClient(config=settings.cards_http_client, logger=logger)
