import os
from collections.abc import Callable
from dataclasses import field
from typing import Any, TypeVar


T = TypeVar("T")


def env_field[T](
    cast_type: Callable[[Any], T],
    key: str,
) -> T:
    """
    Создает поле dataclass по умолчанию во время создания экзмепляра.

    Значение автоматически извлекается из
    переменных окружения и приводится к заданному типу.

    Args:
        cast_type: Функция для преобразования строки из env в нужный тип T.
        key: Название переменной окружения (например, 'DB_PORT').

    Returns:
        Объект `field` с настроенной `default_factory` для динамического
        получения значения при инициализации датакласса.

    Raises:
        KeyError: Если переменная окружения с именем `key` не установлена.
        ValueError: Если `cast_type` не смог преобразовать строку в тип T.

    Example:
        @dataclass
        class Config:
        port: int = env_field(int, "PORT")
    """
    return field(default_factory=lambda: cast_type(os.environ[key]))
