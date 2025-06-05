import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.gateway.apps.users.controllers.users.http import get_user, create_user
from services.users.apps.users.schema.users import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)
from services.users.clients.users.http import UsersHTTPClient, get_users_http_client

users_gateway_router = APIRouter(
    prefix=APIRoutes.USERS,
    tags=[APIRoutes.USERS.as_tag()]
)


@users_gateway_router.get('/{user_id}', response_model=GetUserResponseSchema)
async def get_user_view(
        user_id: uuid.UUID,
        users_http_client: Annotated[UsersHTTPClient, Depends(get_users_http_client)]
):
    return await get_user(user_id, users_http_client)


@users_gateway_router.post('', response_model=CreateUserResponseSchema)
async def create_user_view(
        request: CreateUserRequestSchema,
        users_http_client: Annotated[UsersHTTPClient, Depends(get_users_http_client)]
):
    return await create_user(request, users_http_client)
