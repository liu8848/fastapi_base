from typing import Any,Generic,Type


from common.crud.types import Model, CreateSchema
from common.crud.base_mapper import BaseMapper


class BaseService(Generic[Model]):
    def __init__(self, model: Type[Model]):
        self.model = model
        self.baseMapper= BaseMapper(model)

    async def create_model(
            self,
            obj: CreateSchema,
            **kwargs,
    ) -> Model:
        return await self.baseMapper.create_model(obj, **kwargs)