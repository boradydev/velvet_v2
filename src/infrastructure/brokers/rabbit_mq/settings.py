import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvenBusSettings:
    RABBITMQ_HOST: str = os.environ["RABBITMQ_HOST"]
    RABBITMQ_PORT: str = os.environ["RABBITMQ_PORT"]
    RABBITMQ_USER: str = os.environ["RABBITMQ_USER"]
    RABBITMQ_PASSWORD: str = os.environ["RABBITMQ_PASSWORD"]

    DOMAIN_EVENTS_EXCHANGE: str = os.environ["DOMAIN_EVENTS_EXCHANGE"]

    @property
    def AMQP_URL(self) -> str:
        """URL для подключения библиотек типа aio-pika."""
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@"
            f"{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
        )
