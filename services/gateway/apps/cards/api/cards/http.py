from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.cards.clients.cards.http import CardsHTTPClient, get_cards_http_client
from services.gateway.apps.cards.controllers.cards.http import issue_virtual_card, issue_physical_card
from services.gateway.apps.cards.schema.cards import (
    IssueVirtualCardRequestSchema,
    IssueVirtualCardResponseSchema,
    IssuePhysicalCardRequestSchema,
    IssuePhysicalCardResponseSchema
)
from services.users.clients.users.http import UsersHTTPClient, get_users_http_client

cards_gateway_router = APIRouter(
    prefix=APIRoutes.CARDS,
    tags=[APIRoutes.CARDS.as_tag()]
)


@cards_gateway_router.post(
    '/issue-virtual-card',
    response_model=IssueVirtualCardResponseSchema
)
async def issue_virtual_card_view(
        request: IssueVirtualCardRequestSchema,
        users_http_client: Annotated[UsersHTTPClient, Depends(get_users_http_client)],
        cards_http_client: Annotated[CardsHTTPClient, Depends(get_cards_http_client)]
):
    return await issue_virtual_card(
        request=request,
        users_http_client=users_http_client,
        cards_http_client=cards_http_client
    )


@cards_gateway_router.post(
    '/issue-physical-card',
    response_model=IssuePhysicalCardResponseSchema
)
async def issue_physical_card_view(
        request: IssuePhysicalCardRequestSchema,
        users_http_client: Annotated[UsersHTTPClient, Depends(get_users_http_client)],
        cards_http_client: Annotated[CardsHTTPClient, Depends(get_cards_http_client)]
):
    return await issue_physical_card(
        request=request,
        users_http_client=users_http_client,
        cards_http_client=cards_http_client
    )
