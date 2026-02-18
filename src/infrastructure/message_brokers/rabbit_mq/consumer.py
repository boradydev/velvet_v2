import json
from collections.abc import Awaitable, Callable
from typing import Any, cast

import aio_pika

from src.core.logger import get_logger
from src.presentation.taskiq_event.interfase import IEventConsumer


class RabbitMQConsumer(IEventConsumer):
    def __init__(
        self,
        url: str,
        exchange_name: str,
        queue_name: str,
    ) -> None:
        self._url = url
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._connection: aio_pika.abc.AbstractRobustConnection | None = None

    async def _connect(self) -> aio_pika.abc.AbstractRobustChannel:
        """Создает робастное соединение и канал."""
        self._connection = await aio_pika.connect_robust(self._url)
        channel = await self._connection.channel()

        await channel.set_qos(prefetch_count=1)
        return cast(aio_pika.abc.AbstractRobustChannel, channel)

    async def listen(
        self,
        routing_keys: list[str],
        handler: Callable[[dict[str, Any]], Awaitable[None]],
    ) -> None:
        channel = await self._connect()

        exchange = await channel.declare_exchange(
            self._exchange_name, aio_pika.ExchangeType.TOPIC, durable=True
        )

        queue = await channel.declare_queue(self._queue_name, durable=True)

        for key in routing_keys:
            await queue.bind(exchange, routing_key=key)
            get_logger().info(f"Bound queue {self._queue_name} to {key}")

        get_logger().info(
            f"Consumer started. Waiting for messages in {self._queue_name}..."
        )

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(requeue=True):
                    try:
                        payload = json.loads(message.body.decode())
                        await handler(payload)
                    except Exception as exc:
                        get_logger().error(
                            f"Error processing message {message.message_id}: {exc}"
                        )
                        raise exc

    async def stop(self) -> None:
        if self._connection and not self._connection.is_closed:
            await self._connection.close()
