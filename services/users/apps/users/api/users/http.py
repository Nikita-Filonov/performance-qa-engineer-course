import uuid
from typing import Annotated

from fastapi import APIRouter, Depends

from libs.routes import APIRoutes
from services.users.apps.users.controllers.users.http import get_user, create_user
from services.users.apps.users.schema.users import GetUserResponseSchema, CreateUserRequestSchema, \
    CreateUserResponseSchema
from services.users.services.postgres.repositories.users import UsersRepository, get_users_repository_depends

users_router = APIRouter(
    prefix=APIRoutes.USERS,
    tags=[APIRoutes.USERS.as_tag()]
)


@users_router.get('/{user_id}', response_model=GetUserResponseSchema)
async def get_user_view(
        user_id: uuid.UUID,
        users_repository: Annotated[UsersRepository, Depends(get_users_repository_depends)]
):
    return await get_user(user_id, users_repository)


@users_router.post('', response_model=CreateUserResponseSchema)
async def create_user_view(
        request: CreateUserRequestSchema,
        users_repository: Annotated[UsersRepository, Depends(get_users_repository_depends)]
):
    return await create_user(request, users_repository)
