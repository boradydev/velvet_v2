import asyncio

from uuid6 import uuid7

from src.domain.employees.events import EmployeeRegisteredEvent
from src.infrastructure.message_brokers.rabbit_mq.consumer import RabbitMQConsumer
from src.infrastructure.message_brokers.rabbit_mq.publisher import RabbitMQPublisher
from src.infrastructure.message_brokers.rabbit_mq.settings import EventPublisherSettings


# todo требуется рефаторинг
settings = EventPublisherSettings(
    RABBITMQ_HOST="localhost",
    RABBITMQ_PORT="5672",
    RABBITMQ_USER_PUBLISHER="publisher",
    RABBITMQ_PASSWORD_PUBLISHER="publisher",
    RABBITMQ_USER_CONSUMER="consumer",
    RABBITMQ_PASSWORD_CONSUMER="consumer",
    RABBITMQ_QUEUE="test_integration_queue",
    DOMAIN_EVENTS_EXCHANGE="test_exchange",
)


async def test_rabbit_integration_full_cycle():
    routing_key = "EmployeeRegisteredEvent"

    received_data_future = asyncio.get_running_loop().create_future()
    async def test_handler(payload: dict):
        if not received_data_future.done():
            received_data_future.set_result(payload)

    consumer = RabbitMQConsumer(
        url=settings.AMQP_URL,
        exchange_name=settings.EVENT_BROKER_EXCHANGE,
        queue_name=settings.EVENT_BROKER_QUEUE,
    )
    consumer_task = asyncio.create_task(
        consumer.listen(routing_keys=[routing_key], handler=test_handler)
    )

    try:
        await asyncio.sleep(0.1)

        bus = RabbitMQPublisher(
            url=settings.AMQP_URL, exchange_name=settings.EVENT_BROKER_EXCHANGE
        )
        event_id = uuid7()
        email = "test@test.ru"
        event = EmployeeRegisteredEvent(employee_id=event_id, email=email)

        await bus.publish(event)
        await bus.close()

        received_payload = await asyncio.wait_for(received_data_future, timeout=5.0)

        assert received_payload["email"] == email
        assert received_payload["employee_id"] == str(event_id)

    finally:
        consumer_task.cancel()
        await consumer.stop()
