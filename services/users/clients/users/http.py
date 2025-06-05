import uuid

from httpx import Response

from config import settings
from libs.http.client.base import HTTPClient
from libs.http.client.handlers import handle_http_error, HTTPClientError
from libs.logger import get_logger
from libs.routes import APIRoutes
from services.users.apps.users.schema.users import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)


class UsersHTTPClientError(HTTPClientError):
    pass


class UsersHTTPClient(HTTPClient):
    @handle_http_error(client='UsersHTTPClient', exception=UsersHTTPClientError)
    async def get_user_api(self, user_id: uuid.UUID) -> Response:
        return await self.get(f'{APIRoutes.USERS}/{user_id}')

    @handle_http_error(client='UsersHTTPClient', exception=UsersHTTPClientError)
    async def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        return await self.post(
            APIRoutes.USERS, json=request.model_dump(mode='json', by_alias=True)
        )

    async def get_user(self, user_id: uuid.UUID) -> GetUserResponseSchema:
        response = await self.get_user_api(user_id)
        return GetUserResponseSchema.model_validate_json(response.text)

    async def create_user(
            self,
            email: str,
            last_name: str,
            first_name: str,
            middle_name: str,
            phone_number: str,
    ):
        request = CreateUserRequestSchema(
            email=email,
            last_name=last_name,
            first_name=first_name,
            middle_name=middle_name,
            phone_number=phone_number
        )
        response = await self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)


def get_users_http_client() -> UsersHTTPClient:
    logger = get_logger("USERS_SERVICE_HTTP_CLIENT")
    return UsersHTTPClient(config=settings.users_http_client, logger=logger)
