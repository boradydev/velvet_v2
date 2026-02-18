from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RabbitMQConnectionException(Exception):
    pass