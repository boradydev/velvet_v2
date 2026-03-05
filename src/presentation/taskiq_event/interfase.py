from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any


class IEventConsumer(ABC):
    @abstractmethod
    async def listen(
        self,
        *,
        routing_keys: list[str],
        handler: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        """Начать прослушивание определенных событий."""
        raise NotImplementedError
