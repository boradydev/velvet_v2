import aio_pika
import taskiq_aio_pika


def get_broker(
    url: str,
    exchange_name: str,
    queue_name: str,
) -> taskiq_aio_pika.AioPikaBroker:
    return taskiq_aio_pika.AioPikaBroker(
        url=url,
        exchange_kwargs={
            "name": exchange_name,
            "type": aio_pika.ExchangeType.TOPIC,
            "durable": True,
        },
        queue_kwargs={
            "durable": True,
            "queue_name": queue_name,
        },
        default_delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
    )


