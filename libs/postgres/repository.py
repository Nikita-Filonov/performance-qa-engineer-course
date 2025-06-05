from sqlalchemy.ext.asyncio import AsyncSession

from libs.postgres.mixin_model import MixinModel


class BasePostgresRepository:
    model: type[MixinModel]

    def __init__(self, session: AsyncSession):
        self.session = session
