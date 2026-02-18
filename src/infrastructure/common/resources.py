from logging import Logger

import taskiq_aio_pika

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


class Settings:
    """
    Контейнер конфигурационных настроек приложения.

    Объединяет различные группы настроек (БД, окружение, API) в единый объект
    для удобства передачи между компонентами системы.
    """

    def __init__(
        self,
        postgres: PostgresSettings | None = None,
        app: AppSettings | None = None,
        jwt: JwtSettings | None = None,
        password: PasswordSettings | None = None,
        event_publisher: EventPublisherSettings | None = None,
        event_consumer: EventConsumerSettings | None = None,
        tasks: TasksSettings | None = None,
    ) -> None:
        """
        Инициализирует объект Settings значениями по умолчанию.

        Args:
            event_consumer: Экземпляр класса настроек TaskIQ.
            tasks: Экземпляр класса настроек TaskIQ.
            postgres: Экземпляр класса настроек Postgres.
            app: Экземпляр класса настроек приложения.
            jwt: Экземпляр класса настроек токенов.
            password: Экземпляр класса настроек для паролей.
            event_publisher: Экземпляр класса настроек для шины событий
        """
        self.postgres = postgres or PostgresSettings()
        self.app = app or AppSettings()
        self.jwt = jwt or JwtSettings()
        self.password = password or PasswordSettings()
        self.event_publisher = event_publisher or EventPublisherSettings()
        self.event_consumer = event_consumer or EventConsumerSettings()
        self.tasks = tasks or TasksSettings()


class AppResources:
    """
    Контейнер активных ресурсов и клиентов приложения.

    Предназначен для хранения инициализированных соединений, пулов и объектов,
    чей жизненный цикл управляется в `lifespan` приложения.
    """

    def __init__(
        self,
        settings: Settings,
        interactors: InteractorResources,
        tasks_broker: taskiq_aio_pika.AioPikaBroker,
        logger: Logger,
    ) -> None:
        """
        Инициализирует контейнер ресурсов.

        Args:
            settings: Сконфигурированный объект Settings.
            interactors: Готовый к работе клиент InteractorFactory.
            tasks_broker: Экземпляр taskiq_event требуется хранить ссылку для запуска задач.
            logger: Готовый объект логгера.
        """
        self.settings = settings
        self.interactors = interactors
        self.tasks_broker = tasks_broker
        self.logger = logger
