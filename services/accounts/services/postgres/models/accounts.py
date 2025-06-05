import uuid
from enum import StrEnum

from sqlalchemy import Column, UUID, String, Float
from sqlalchemy.orm import Mapped

from libs.base.enums import ProtoEnum
from libs.postgres.mixin_model import MixinModel


class AccountType(ProtoEnum, StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    DEBIT_CARD = "DEBIT_CARD"
    CREDIT_CARD = "CREDIT_CARD"
    DEPOSIT = "DEPOSIT"
    SAVINGS = "SAVINGS"


class AccountStatus(ProtoEnum, StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    ACTIVE = "ACTIVE"
    PENDING_CLOSURE = "PENDING_CLOSURE"
    CLOSED = "CLOSED"


class AccountsModel(MixinModel):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = Column(UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = Column(String(length=50), nullable=False)
    status: Mapped[str] = Column(String(length=50), nullable=False)
    user_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)
    balance: Mapped[float] = Column(Float, nullable=False)
