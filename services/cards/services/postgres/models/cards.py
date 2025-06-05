import uuid
from datetime import date
from enum import StrEnum

from sqlalchemy import Column, UUID, String, Date
from sqlalchemy.orm import Mapped

from libs.base.enums import ProtoEnum
from libs.postgres.mixin_model import MixinModel


class CardType(ProtoEnum, StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    VIRTUAL = "VIRTUAL"
    PHYSICAL = "PHYSICAL"


class CardStatus(ProtoEnum, StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    BLOCKED = "BLOCKED"


class CardPaymentSystem(ProtoEnum, StrEnum):
    UNSPECIFIED = "UNSPECIFIED"
    MASTERCARD = "MASTERCARD"
    VISA = "VISA"


class CardsModel(MixinModel):
    __tablename__ = "cards"

    id: Mapped[uuid.UUID] = Column(UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    pin: Mapped[int] = Column(String(length=10), nullable=False)
    cvv: Mapped[int] = Column(String(length=10), nullable=False)
    type: Mapped[str] = Column(String(length=50), nullable=False)
    status: Mapped[str] = Column(String(length=50), nullable=False)
    account_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)
    card_number: Mapped[int] = Column(String(length=50), nullable=False)
    card_holder: Mapped[str] = Column(String(length=250), nullable=False)
    expiry_date: Mapped[date] = Column(Date, nullable=False)
    payment_system: Mapped[str] = Column(String(length=50), nullable=False)
