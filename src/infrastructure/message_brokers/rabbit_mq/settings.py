from dataclasses import dataclass

from src.core.settings.environ import env_field


@dataclass(frozen=True, slots=True)
class EventPublisherSettings:
    EVENT_BROKER_HOST: str = env_field(str, "EVENT_BROKER_HOST")
    EVENT_BROKER_PORT: str = env_field(str, "EVENT_BROKER_PORT")
    EVENT_BROKER_USER: str = env_field(str, "EVENT_BROKER_USER")
    EVENT_BROKER_PASSWORD: str = env_field(str, "EVENT_BROKER_PASSWORD")
    EVENT_BROKER_EXCHANGE: str = env_field(str, "EVENT_BROKER_EXCHANGE")

    @property
    def AMQP_URL(self) -> str:
        return (
            f"amqp://{self.EVENT_BROKER_USER}:{self.EVENT_BROKER_PASSWORD}@"
            f"{self.EVENT_BROKER_HOST}:{self.EVENT_BROKER_PORT}/"
        )
