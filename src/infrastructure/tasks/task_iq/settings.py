from dataclasses import dataclass

from src.core.settings.environ import env_field


@dataclass(frozen=True, slots=True)
class TasksSettings:
    TASK_BROKER_HOST: str = env_field(str, "TASK_BROKER_HOST")
    TASK_BROKER_PORT: str = env_field(str, "TASK_BROKER_PORT")
    TASK_BROKER_USER: str = env_field(str, "TASK_BROKER_USER")
    TASK_BROKER_PASSWORD: str = env_field(str, "TASK_BROKER_PASSWORD")
    TASK_BROKER_EXCHANGE: str = env_field(str, "TASK_BROKER_EXCHANGE")
    TASK_BROKER_QUEUE: str = env_field(str, "TASK_BROKER_QUEUE")

    @property
    def AMQP_URL(self) -> str:
        return (
            f"amqp://{self.TASK_BROKER_USER}:{self.TASK_BROKER_PASSWORD}@"
            f"{self.TASK_BROKER_HOST}:{self.TASK_BROKER_PORT}/"
        )


@dataclass(frozen=True, slots=True)
class EventConsumerSettings:
    EVENT_BROKER_HOST: str = env_field(str, "EVENT_BROKER_HOST")
    EVENT_BROKER_PORT: str = env_field(str, "EVENT_BROKER_PORT")
    EVENT_BROKER_CONSUMER_USER: str = env_field(str, "EVENT_BROKER_CONSUMER_USER")
    EVENT_BROKER_CONSUMER_PASSWORD: str = env_field(
        str, "EVENT_BROKER_CONSUMER_PASSWORD"
    )
    EVENT_BROKER_EXCHANGE: str = env_field(str, "EVENT_BROKER_EXCHANGE")
    EVENT_BROKER_QUEUE: str = env_field(str, "EVENT_BROKER_QUEUE")

    @property
    def AMQP_URL(self) -> str:
        return (
            f"amqp://{self.EVENT_BROKER_CONSUMER_USER}:"
            f"{self.EVENT_BROKER_CONSUMER_PASSWORD}@"
            f"{self.EVENT_BROKER_HOST}:{self.EVENT_BROKER_PORT}/"
        )
