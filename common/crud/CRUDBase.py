
from typing import Generic,Type

from common.crud.types import Model,CreateSchema,UpdateSchema

class CRUDBase(Generic[Model]):
    def __init__(self, model: Type[Model]) -> None:
        self.model = model