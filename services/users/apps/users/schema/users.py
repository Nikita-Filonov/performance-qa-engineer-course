from pydantic import EmailStr, UUID4

from libs.schema.base import BaseSchema


# TODO добавить редис можно для например документов. Чтобы каждый раз не ходить за ними


class UserSchema(BaseSchema):
    id: UUID4
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str


class GetUserResponseSchema(BaseSchema):
    user: UserSchema


class CreateUserRequestSchema(BaseSchema):
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str
    phone_number: str


class CreateUserResponseSchema(BaseSchema):
    user: UserSchema
