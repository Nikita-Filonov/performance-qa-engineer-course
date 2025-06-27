import uuid

from fastapi import APIRouter

from libs.routes import APIRoutes
from services.mock.apps.users.mock import loader
from services.users.apps.users.schema.users import (
    GetUserResponseSchema,
    CreateUserRequestSchema,
    CreateUserResponseSchema
)

users_mock_router = APIRouter(
    prefix=APIRoutes.USERS,
    tags=[APIRoutes.USERS.as_tag()]
)


@users_mock_router.get('/{user_id}', response_model=GetUserResponseSchema)
async def get_user_view(user_id: uuid.UUID):
    return loader.load_http("get_user/default.json", GetUserResponseSchema)


@users_mock_router.post('', response_model=CreateUserResponseSchema)
async def create_user_view(request: CreateUserRequestSchema):
    return loader.load_http("create_user/default.json", CreateUserResponseSchema)
