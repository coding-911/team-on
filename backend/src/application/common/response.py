from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None

    @classmethod
    def success(cls, data: Optional[T] = None, message: str = "Success") -> "ApiResponse[T]":
        return cls(
            code=1000,
            message=message,
            data=data
        )

    @classmethod
    def error(cls, code: int, message: str) -> "ApiResponse[None]":
        return cls(
            code=code,
            message=message,
            data=None
        ) 