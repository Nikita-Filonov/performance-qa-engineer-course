from pydantic import UUID4

from libs.schema.base import BaseSchema
from services.cards.apps.cards.schema.cards import CardSchema


class IssueVirtualCardRequestSchema(BaseSchema):
    user_id: UUID4
    account_id: UUID4


class IssueVirtualCardResponseSchema(BaseSchema):
    card: CardSchema


class IssuePhysicalCardRequestSchema(BaseSchema):
    user_id: UUID4
    account_id: UUID4


class IssuePhysicalCardResponseSchema(BaseSchema):
    card: CardSchema
