import uuid

from sqlalchemy import Column, UUID, String
from sqlalchemy.orm import Mapped

from libs.postgres.mixin_model import MixinModel


class UsersModel(MixinModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = Column(UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = Column(String(length=250), nullable=False, unique=True)
    last_name: Mapped[str] = Column(String(length=50), nullable=False)
    first_name: Mapped[str] = Column(String(length=50), nullable=False)
    middle_name: Mapped[str] = Column(String(length=50), nullable=False)
    phone_number: Mapped[str] = Column(String(length=50), nullable=False)
