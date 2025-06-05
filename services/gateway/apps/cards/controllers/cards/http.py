from fastapi import HTTPException

from services.cards.clients.cards.http import CardsHTTPClient, CardsHTTPClientError
from services.gateway.apps.cards.schema.cards import (
    IssueVirtualCardRequestSchema,
    IssueVirtualCardResponseSchema,
    IssuePhysicalCardRequestSchema,
    IssuePhysicalCardResponseSchema
)
from services.users.clients.users.http import UsersHTTPClient, UsersHTTPClientError


async def issue_virtual_card(
        request: IssueVirtualCardRequestSchema,
        users_http_client: UsersHTTPClient,
        cards_http_client: CardsHTTPClient
) -> IssueVirtualCardResponseSchema:
    try:
        get_user_response = await users_http_client.get_user(request.user_id)
    except UsersHTTPClientError as error:
        raise HTTPException(
            detail=f"Issue virtual card: {error.details}",
            status_code=error.status_code
        )

    try:
        create_card_response = await cards_http_client.create_virtual_card(
            last_name=get_user_response.user.last_name,
            first_name=get_user_response.user.first_name,
            account_id=request.account_id
        )
    except CardsHTTPClientError as error:
        raise HTTPException(
            detail=f"Issue physical card: {error.details}",
            status_code=error.status_code
        )

    return IssueVirtualCardResponseSchema(card=create_card_response.card)


async def issue_physical_card(
        request: IssuePhysicalCardRequestSchema,
        users_http_client: UsersHTTPClient,
        cards_http_client: CardsHTTPClient
) -> IssuePhysicalCardResponseSchema:
    try:
        get_user_response = await users_http_client.get_user(request.user_id)
    except UsersHTTPClientError as error:
        raise HTTPException(
            detail=f"Issue physical card: {error.details}",
            status_code=error.status_code
        )

    try:
        create_card_response = await cards_http_client.create_physical_card(
            last_name=get_user_response.user.last_name,
            first_name=get_user_response.user.first_name,
            account_id=request.account_id
        )
    except CardsHTTPClientError as error:
        raise HTTPException(
            detail=f"Issue physical card: {error.details}",
            status_code=error.status_code
        )

    return IssuePhysicalCardResponseSchema(card=create_card_response.card)
