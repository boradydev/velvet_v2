from dataclasses import dataclass

from src.core.timezone import Timestamp


@dataclass(kw_only=True, frozen=True)
class BaseDomainEvent:
    """Базовый класс для всех событий домена."""

    created_at: Timestamp
