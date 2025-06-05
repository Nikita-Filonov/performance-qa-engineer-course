import uuid
from typing import Self

from fastapi import Query

from libs.schema.base import BaseSchema
from libs.schema.query import QuerySchema
from services.accounts.apps.accounts.schema.accounts import AccountSchema
from services.cards.apps.cards.schema.cards import CardSchema


class AccountViewSchema(BaseSchema):
    cards: list[CardSchema]
    account: AccountSchema


class GetAccountsQuerySchema(QuerySchema):
    user_id: uuid.UUID

    @classmethod
    async def as_query(cls, user_id: uuid.UUID = Query(alias="userId")) -> Self:
        return GetAccountsQuerySchema(user_id=user_id)


class GetAccountsResponseSchema(BaseSchema):
    accounts: list[AccountViewSchema]


class OpenSavingsAccountRequestSchema(BaseSchema):
    user_id: uuid.UUID


class OpenSavingsAccountResponseSchema(BaseSchema):
    account: AccountViewSchema


class OpenDepositAccountRequestSchema(BaseSchema):
    user_id: uuid.UUID


class OpenDepositAccountResponseSchema(BaseSchema):
    account: AccountViewSchema


class OpenDebitCardAccountRequestSchema(BaseSchema):
    user_id: uuid.UUID


class OpenDebitCardAccountResponseSchema(BaseSchema):
    account: AccountViewSchema


class OpenCreditCardAccountRequestSchema(BaseSchema):
    user_id: uuid.UUID


class OpenCreditCardAccountResponseSchema(BaseSchema):
    account: AccountViewSchema
