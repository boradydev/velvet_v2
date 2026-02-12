from logging import Logger

from fastapi.requests import Request

from src.core.settings.app import AppSettings
from src.infrastructure.auth.jwt.settings import JwtSettings
from src.infrastructure.db.postgres.settings import PostgresSettings
from src.infrastructure.factories.interactors.base import InteractorResources
from src.infrastructure.security.settings import PasswordSettings


class Settings:
    """
    Контейнер конфигурационных настроек приложения.

    Объединяет различные группы настроек (БД, окружение, API) в единый объект
    для удобства передачи между компонентами системы.

    Attributes:
        postgres: Настройки подключения к PostgreSQL.
        app: Общие настройки приложения (название, версия, лимиты).
    """

    postgres: PostgresSettings
    app: AppSettings
    jwt: JwtSettings
    password: PasswordSettings

    def __init__(
        self,
        postgres: PostgresSettings | None = None,
        app: AppSettings | None = None,
        jwt: JwtSettings | None = None,
        password: PasswordSettings | None = None,
    ) -> None:
        """
        Инициализирует объект Settings значениями по умолчанию.

        Args:
            postgres: Экземпляр класса настроек Postgres.
            app: Экземпляр класса настроек приложения.
            jwt: Экземпляр класса настроек токенов.
            password: Экземпляр класса настроек для паролей.
        """
        self.postgres = postgres or PostgresSettings()
        self.app = app or AppSettings()
        self.jwt = jwt or JwtSettings()
        self.password = password or PasswordSettings()


class AppResources:
    """
    Контейнер активных ресурсов и клиентов приложения.

    Предназначен для хранения инициализированных соединений, пулов и объектов,
    чей жизненный цикл управляется в `lifespan` приложения.

    Attributes:
        settings: Ссылка на объект настроек.
        interactors: Инициализированный клиент или пул базы данных.
    """

    settings: Settings
    interactors: InteractorResources
    logger: Logger

    def __init__(
        self,
        settings: Settings,
        interactors: InteractorResources,
        logger: Logger,
    ) -> None:
        """
        Инициализирует контейнер ресурсов.

        Args:
            settings: Сконфигурированный объект Settings.
            interactors: Готовый к работе клиент InteractorFactory.
            logger: Готовый объект логгера.
        """
        self.settings = settings
        self.interactors = interactors
        self.logger = logger


def get_resources(request: Request) -> AppResources:
    """
    Извлекает ресурсы приложения из состояния (state) запроса.

    Используется в качестве зависимости (Dependency) в FastAPI роутерах
    для доступа к базе данных и конфигурации.

    Args:
        request: Объект входящего HTTP-запроса FastAPI.

    Returns:
        Объект AppResources, содержащий текущие настройки и подключения.
    """
    return request.app.state.resources
