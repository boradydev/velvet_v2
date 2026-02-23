from collections.abc import Callable
from typing import Any, Protocol

from src.application.common.interfaces import IEventPublisher
from src.application.employees import cases
from src.domain.common.interfaces.services_abc import (
    ILogger,
    IPasswordService,
    ITokenService,
)


class IEmployeeUseCaseFactory(Protocol):
    """Интерфейс фабрики интеракторов домена "Сотрудники" (Employees)."""

    def create_register_case(self) -> cases.Register: ...

    def create_confirm_register_case(self) -> cases.ConfirmRegister: ...

    def create_login_case(self) -> cases.Login: ...

    def create_resend_case(self) -> cases.ReSendCodeConfirmation: ...


class IEmployeeUseCaseResources(Protocol):
    """Контракт ресурсов (БД, сервисы) для сборки интеракторов (Employees)."""

    @property
    def session_factory(self) -> Callable[[], Any]:
        """Фабрика сессий. Возвращает объект сессии (AsyncSession) при вызове."""
        ...

    @property
    def token_service(self) -> ITokenService:
        """Сервис для работы с JWT или OAuth2 токенами."""
        ...

    @property
    def password_service(self) -> IPasswordService:
        """Сервис хеширования и проверки паролей."""
        ...

    @property
    def event_publisher(self) -> IEventPublisher:
        """Брокер событий домена."""
        ...

    @property
    def logger(self) -> ILogger:
        """Логгер."""
        ...
