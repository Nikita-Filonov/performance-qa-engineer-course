from libs.postgres.create_model import CreateModel
from libs.postgres.delete_model import DeleteModel
from libs.postgres.filter_model import FilterModel
from libs.postgres.update_model import UpdateModel


class MixinModel(
    FilterModel,
    CreateModel,
    UpdateModel,
    DeleteModel
):
    __abstract__ = True
