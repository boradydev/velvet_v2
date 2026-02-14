import asyncio
import json
from dataclasses import asdict

import aio_pika

from src.application.base.interfaces import IEventBus
from src.domain.base.events import BaseDomainEvent
from src.infrastructure.brokers.rabbit_mq.exceptions import RabbitMQConnectionException


class RabbitMQEventBus(IEventBus):
    def __init__(
        self,
        url: str,
        exchange_name: str,
    ) -> None:
        self._connection_url = url
        self._exchange_name = exchange_name
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None
        self._channel: aio_pika.abc.AbstractChannel | None = None
        self._exchange: aio_pika.abc.AbstractExchange | None = None
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        async with self._lock:
            if self._connection is None or self._connection.is_closed:
                self._connection = await aio_pika.connect_robust(self._connection_url)

            if self._channel is None or self._channel.is_closed:
                self._channel = await self._connection.channel()
                self._exchange = await self._channel.declare_exchange(
                    self._exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
                )

    async def publish(self, event: BaseDomainEvent) -> None:
        return await self.publish_many([event])

    async def publish_many(self, events: list[BaseDomainEvent]) -> None:
        if not events:
            return

        if self._exchange is None or self._channel is None or self._channel.is_closed:
            await self.connect()

        if self._exchange is None or self._channel is None or self._connection is None:
            raise RabbitMQConnectionException

        for event in events:
            routing_key = event.__class__.__name__
            message_body = json.dumps(asdict(event), default=str).encode()
            await self._exchange.publish(
                aio_pika.Message(body=message_body, content_type="application/json"),
                routing_key=routing_key,
            )

    async def close(self) -> None:
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
        else:
            raise RabbitMQConnectionException