from typing import TypeVar

from pydantic import BaseModel

Model=TypeVar("Model")

CreateSchema=TypeVar("CreateSchema",bound=BaseModel)
UpdateSchema=TypeVar("UpdateSchema",bound=BaseModel)