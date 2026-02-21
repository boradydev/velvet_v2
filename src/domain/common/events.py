from dataclasses import dataclass, field
from datetime import datetime

from src.core.timezone import get_timestamp


@dataclass(kw_only=True, frozen=True)
class BaseDomainEvent:
    """Базовый класс для всех событий домена."""

    timestamp: datetime = field(default_factory=get_timestamp)
