import uuid

from fastapi import HTTPException, status

from services.accounts.clients.accounts.http import AccountsHTTPClient, AccountsHTTPClientError
from services.cards.apps.cards.schema.cards import (
    CardSchema,
    GetCardResponseSchema,
    GetCardsQuerySchema,
    GetCardsResponseSchema,
    CreateCardRequestSchema,
    CreateCardResponseSchema
)
from services.cards.services.postgres.repositories.cards import CardsRepository, CreateCardDict


async def get_card(
        card_id: uuid.UUID,
        cards_repository: CardsRepository
) -> GetCardResponseSchema:
    card = await cards_repository.get_by_id(card_id)
    if not card:
        raise HTTPException(
            detail=f"Card with id {card_id} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )

    return GetCardResponseSchema(card=CardSchema.model_validate(card))


async def get_cards(
        query: GetCardsQuerySchema,
        cards_repository: CardsRepository
) -> GetCardsResponseSchema:
    cards = await cards_repository.filter(account_id=query.account_id)

    return GetCardsResponseSchema(cards=[CardSchema.model_validate(card) for card in cards])


async def create_card(
        request: CreateCardRequestSchema,
        cards_repository: CardsRepository,
        accounts_http_client: AccountsHTTPClient,
) -> CreateCardResponseSchema:
    try:
        get_account_response = await accounts_http_client.get_account(request.account_id)
    except AccountsHTTPClientError as error:
        raise HTTPException(
            detail=f"Create card: {error.details}",
            status_code=error.status_code
        )

    card = await cards_repository.create(
        CreateCardDict(
            pin=request.pin,
            cvv=request.cvv,
            type=request.type,
            status=request.status,
            account_id=get_account_response.account.id,
            card_number=request.card_number,
            card_holder=request.card_holder,
            expiry_date=request.expiry_date,
            payment_system=request.payment_system
        )
    )

    return CreateCardResponseSchema(card=CardSchema.model_validate(card))
