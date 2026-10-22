from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T", default=dict)


class APIResponse(BaseModel, Generic[T]):
    status: str
    message: str
    data: T | None = None
