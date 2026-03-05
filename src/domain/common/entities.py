from dataclasses import dataclass, field

from src.domain.common.events import BaseDomainEvent


@dataclass
class BaseEntity:
    """
    Базовая доменная сущность.

    Attributes:
        _events (List[BaseDomainEvent]): Список накопленных доменных событий.
            Используемые параметры field:
                ``init=False``: Поле исключено из __init__, так как события
                    генерируются внутри методов сущности, а не передаются извне
                ``repr=False``: Поле исключено из строкового представления (repr),
                    чтобы не засорять логи техническими деталями событий
                ``compare=False``: Поле не участвует в сравнении объектов (==), так как
                    наличие или отсутствие событий не меняет идентичность сущности
                ``default_factory=list``: Гарантирует создание нового пустого списка
                    для каждого экземпляра, избегая проблемы разделяемого состояния
    """

    _events: list[BaseDomainEvent] = field(
        init=False,
        repr=False,
        compare=False,
        default_factory=list,
    )

    def _add_event(self, event: BaseDomainEvent) -> None:
        """Добавляет событие."""
        self._events.append(event)

    def pull_events(self) -> list[BaseDomainEvent]:
        """Забирает все накопленные события и очищает список."""
        events = self._events.copy()
        self._events.clear()
        return events
