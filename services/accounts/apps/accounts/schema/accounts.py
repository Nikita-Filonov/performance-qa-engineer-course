from typing import Self

from fastapi import Query
from pydantic import UUID4, Field, ConfigDict
from pydantic.alias_generators import to_camel

from libs.schema.base import BaseSchema
from libs.schema.query import QuerySchema
from services.accounts.services.postgres.models.accounts import AccountType, AccountStatus


class AccountSchema(BaseSchema):
    id: UUID4
    type: AccountType
    status: AccountStatus
    user_id: UUID4
    balance: float


class GetAccountResponseSchema(BaseSchema):
    account: AccountSchema


class GetAccountsQuerySchema(QuerySchema):
    user_id: UUID4

    @classmethod
    async def as_query(cls, user_id: UUID4 = Query(alias="userId")) -> Self:
        return GetAccountsQuerySchema(user_id=user_id)


class GetAccountsResponseSchema(BaseSchema):
    accounts: list[AccountSchema]


class CreateAccountRequestSchema(BaseSchema):
    model_config = ConfigDict(alias_generator=to_camel)

    type: AccountType
    status: AccountStatus
    user_id: UUID4 = Field(alias="userId")
    balance: float


class CreateAccountResponseSchema(BaseSchema):
    account: AccountSchema


class UpdateAccountBalanceRequestSchema(BaseSchema):
    balance: float
    account_id: UUID4


class UpdateAccountBalanceResponseSchema(BaseSchema):
    account: AccountSchema
