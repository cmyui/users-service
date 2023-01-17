from typing import Any
from typing import Generic
from typing import Literal
from typing import TypeVar

from app.common import json
from app.common.errors import ServiceError
from pydantic.generics import GenericModel

T = TypeVar("T")


class Success(GenericModel, Generic[T]):
    status: Literal["success"]
    data: T
    meta: dict[str, Any]  # TODO: non-total typeddict?


def success(
    content: Any,
    status_code: int = 200,
    headers: dict[str, Any] | None = None,
    meta: dict[str, Any] | None = None,
) -> Any:
    if meta is None:
        meta = {}
    data = {"status": "success", "data": content, "meta": meta}
    return json.ORJSONResponse(data, status_code, headers)


class ErrorResponse(GenericModel, Generic[T]):
    status: Literal["error"]
    error: T
    message: str


def failure(
    error: ServiceError,
    message: str,
    status_code: int = 400,
    headers: dict | None = None,
) -> Any:
    data = {"status": "error", "error": error, "message": message}
    return json.ORJSONResponse(data, status_code, headers)
