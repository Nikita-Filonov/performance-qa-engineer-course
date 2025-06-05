from typing import Self

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class QuerySchema(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    @classmethod
    async def as_query(cls, **kwargs) -> Self:
        raise NotImplementedError("Override this method in child model")
