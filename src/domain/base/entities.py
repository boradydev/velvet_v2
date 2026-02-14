from dataclasses import dataclass, field

from uuid6 import UUID

from src.domain.base.events import BaseDomainEvent


@dataclass
class BaseEntity:
    id: UUID
    _events: list[BaseDomainEvent] = field(
        init=False, repr=False, compare=False, default_factory=list
    )

    def _add_event(self, event: BaseDomainEvent) -> None:
        self._events.append(event)

    def pull_events(self) -> list[BaseDomainEvent]:
        """Забирает все накопленные события и очищает список."""
        events = self._events
        self._events.clear()
        return events

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id
