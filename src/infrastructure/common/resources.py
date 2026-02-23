from dataclasses import dataclass, field

from taskiq_aio_pika import AioPikaBroker

from src.core.settings.app import AppSettings
from src.domain.common.interfaces.services_abc import ILogger
from src.infrastructure.auth.jwt.settings import JwtSettings
from src.infrastructure.db.postgres.settings import PostgresSettings
from src.infrastructure.factories.cases.common import UseCaseResources
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
    cases: UseCaseResources
    tasks_broker: AioPikaBroker
