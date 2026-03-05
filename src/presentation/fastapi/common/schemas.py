from typing import TypeVar

import inflection
from pydantic import BaseModel, ConfigDict, Field

from src.core.timezone import Timestamp, get_now


class BaseSchemaOrigin(BaseModel):
    """Базовая схема с поддержкой snake_case."""


class BaseSchema(BaseSchemaOrigin):
    """Базовая схема с поддержкой camelCase."""

    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=lambda s: inflection.camelize(s, uppercase_first_letter=False),
        populate_by_name=True,
    )


class Meta(BaseSchema):
    """
    Метаданные ответа.

    Attributes:
        timestamp: Время формирования ответа в формате UTC.
    """

    timestamp: Timestamp = Field(default_factory=get_now)


DataType = TypeVar("DataType", bound=BaseSchema)


class BaseResponse(BaseSchema):
    """
    Абстрактный каркас стандартного API ответа.

    Attributes:
        message: Опциональное текстовое сообщение (например, текст ошибки или успеха).
        meta: Объект с метаданными (таймстамп и прочее).
    """

    message: str | None = None
    meta: Meta = Field(default_factory=Meta)


class NullDataResponse(BaseResponse):
    """
    Ответ без полезной нагрузки (Data is None).

    Используется для операций удаления или пустых результатов.
    """

    data: None = None


class StandardResponse[DataType: BaseSchema](BaseResponse):
    """
    Типизированный успешный ответ API.

    Generic:
        ResponseType: Класс схемы, описывающий структуру поля data.
    """

    data: DataType


class ErrorResponse(BaseSchema):
    detail: str
    meta: Meta = Field(default_factory=Meta)
