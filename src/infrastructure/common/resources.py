from dataclasses import dataclass, field

from taskiq_aio_pika import AioPikaBroker

from src.application.services.logger import ILogger
from src.core.settings.app import AppSettings
from src.infrastructure.auth.jwt.settings import JwtSettings
from src.infrastructure.db.postgres.settings import PostgresSettings
from src.infrastructure.factories.interactors.base import InteractorResources
from src.infrastructure.message_brokers.rabbit_mq.settings import EventPublisherSettings
from src.infrastructure.security.settings import PasswordSettings
from src.infrastructure.tasks.task_iq.settings import (
    EventConsumerSettings,
    TasksSettings,
)


@dataclass(frozen=True, slots=True)
class Settings:
    postgres: PostgresSettings = field(default_factory=PostgresSettings)
    app: AppSettings = field(default_factory=AppSettings)
    jwt: JwtSettings = field(default_factory=JwtSettings)
    password: PasswordSettings = field(default_factory=PasswordSettings)
    event_publisher: EventPublisherSettings = field(
        default_factory=EventPublisherSettings
    )
    event_consumer: EventConsumerSettings = field(default_factory=EventConsumerSettings)
    tasks: TasksSettings = field(default_factory=TasksSettings)


@dataclass(frozen=True, slots=True)
class AppState:
    settings: Settings
    logger: ILogger


@dataclass(frozen=True, slots=True)
class LifespanState:
    interactors: InteractorResources
    tasks_broker: AioPikaBroker
