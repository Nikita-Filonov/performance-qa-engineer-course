import uuid

from fastapi import HTTPException

from services.users.apps.users.schema.users import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)
from services.users.clients.users.http import UsersHTTPClient, UsersHTTPClientError


async def get_user(user_id: uuid.UUID, users_http_client: UsersHTTPClient) -> GetUserResponseSchema:
    try:
        return await users_http_client.get_user(user_id)
    except UsersHTTPClientError as error:
        raise HTTPException(
            detail=f"Get user: {error.details}",
            status_code=error.status_code
        )


async def create_user(
        request: CreateUserRequestSchema,
        users_http_client: UsersHTTPClient
) -> CreateUserResponseSchema:
    try:
        return await users_http_client.create_user(**request.model_dump(mode='json'))
    except UsersHTTPClientError as error:
        raise HTTPException(
            detail=f"Create user: {error.details}",
            status_code=error.status_code
        )
