from abc import ABC, abstractmethod

from src.domain.base.events import BaseDomainEvent


class IEventBus(ABC):
    """
    Интерфейс шины событий.

    Отвечает за доставку доменных событий соответствующим подписчикам.
    """

    @abstractmethod
    async def publish(self, event: BaseDomainEvent) -> None:
        """
        Публикует одно событие.

        Находит всех подписчиков этого типа события и вызывает их.
        """

    @abstractmethod
    async def publish_many(self, events: list[BaseDomainEvent]) -> None:
        """
        Оптимизированная публикация списка событий.

        Полезна для вызова из UOW.commit(events=...).
        """
