from collections.abc import Callable
from datetime import UTC, datetime, timedelta


type Timestamp = datetime
type Timedelta = timedelta


def get_now() -> Timestamp:
    """Глобальная функция, точка получения текущего времени UTC."""
    return datetime.now(UTC)


def get_time_service(
    time_provider: Callable[[],Timestamp] | None = None,
) -> Callable[[], Timestamp]:
    """
    Создает обертку над провайдером времени для инъекции зависимостей.

    Используется для отделения бизнес-логики от системных часов. Позволяет
    передавать реальное время в приложении и фиксированное (замороженное)
    время в Unit-тестах.

    Args:
        time_provider: Функция без аргументов, возвращающая объект datetime (Timestamp).
            Обычно это `datetime.now(UTC)` или лямбда-функция с константой.

    Returns:
        Callable[[], Timestamp]: Возвращает ту же функцию-провайдер, готовую к вызову.

    Examples:
        Использование реального времени в приложении:
        >>> now = get_time_service(time_provider=lambda: datetime.now(UTC))
        >>> print(now())
        2026-02-24 12:00:00...

        Использование фиксированного времени в тестах (заморозка):
        >>> fixed_time = datetime(2026, 2, 24, 12, 0, tzinfo=UTC)
        >>> now = get_time_service(time_provider=lambda: fixed_time)
        >>> print(now())
        2026-02-24 12:00:00+00:00
    """
    return time_provider or get_now
