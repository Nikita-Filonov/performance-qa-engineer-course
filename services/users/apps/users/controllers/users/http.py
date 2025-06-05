import uuid

from fastapi import HTTPException, status

from services.users.apps.users.schema.users import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema, \
    GetUserResponseSchema
from services.users.services.postgres.repositories.users import UsersRepository


async def get_user(
        user_id: uuid.UUID,
        users_repository: UsersRepository
) -> GetUserResponseSchema:
    user = await users_repository.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )

    return GetUserResponseSchema(user=UserSchema.model_validate(user))


async def create_user(
        request: CreateUserRequestSchema,
        users_repository: UsersRepository
) -> CreateUserResponseSchema:
    user = await users_repository.get_by_email(request.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"User with email {request.email} already exists"
        )

    user = await users_repository.create(request.model_dump(mode='json'))

    return CreateUserResponseSchema(user=UserSchema.model_validate(user))
