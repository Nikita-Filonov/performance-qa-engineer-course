import uuid
from datetime import datetime
from enum import StrEnum
from typing import Self

from sqlalchemy import Column, UUID, DateTime, Float, String, func, case
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.functions import coalesce

from libs.base.enums import ProtoEnum
from libs.postgres.mixin_model import MixinModel


class OperationType(ProtoEnum, StrEnum):
    FEE = "FEE"
    TOP_UP = "TOP_UP"
    PURCHASE = "PURCHASE"
    CASHBACK = "CASHBACK"
    TRANSFER = "TRANSFER"
    BILL_PAYMENT = "BILL_PAYMENT"
    CASH_WITHDRAWAL = "CASH_WITHDRAWAL"

    @classmethod
    def list_spent(cls) -> list[Self]:
        return [
            cls.FEE,
            cls.TRANSFER,
            cls.PURCHASE,
            cls.BILL_PAYMENT,
            cls.CASH_WITHDRAWAL
        ]

    @classmethod
    def list_received(cls) -> list[Self]:
        return [cls.TOP_UP]

    @classmethod
    def list_cashback(cls) -> list[Self]:
        return [cls.CASHBACK]


class OperationStatus(ProtoEnum, StrEnum):
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    IN_PROGRESS = "IN_PROGRESS"
    UNSPECIFIED = "UNSPECIFIED"

    def is_success(self) -> bool:
        return self in [self.IN_PROGRESS, self.COMPLETED]


class OperationsModel(MixinModel):
    __tablename__ = "operations"

    id: Mapped[uuid.UUID] = Column(UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    type: Mapped[str] = Column(String(length=50), nullable=False)
    status: Mapped[str] = Column(String(length=50), nullable=False)
    amount: Mapped[float] = Column(Float, nullable=False)
    card_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)
    category: Mapped[str] = Column(String(length=50), nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, nullable=False)
    account_id: Mapped[uuid.UUID] = Column(UUID, nullable=False)

    @classmethod
    def aggregate_amount_by_types(cls, types: list[OperationType]) -> coalesce:
        amount = func.sum(case((cls.type.in_(types), OperationsModel.amount), else_=0.0))
        return func.coalesce(amount, 0.0)
