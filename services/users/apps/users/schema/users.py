from pydantic import EmailStr, UUID4

from libs.schema.base import BaseSchema


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
