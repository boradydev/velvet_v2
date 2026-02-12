from collections.abc import Callable
from typing import Any, Protocol

from src.application.employees import interactors
from src.application.services.code import IConfirmationCodeService
from src.application.services.logger import ILogger
from src.application.services.send import IEmailService
from src.application.services.token import ITokenService
from src.domain.employees.interfaces import IPasswordService


class IEmployeeInteractorFactory(Protocol):
    """Интерфейс фабрики интеракторов домена "Сотрудники" (Employees)."""

    def create_register_interactor(self) -> interactors.RegisterInteractor:
        """Создает сценарий регистрации нового сотрудника."""

    def create_login_interactor(self) -> interactors.LoginInteractor:
        """Создает сценарий аутентификации сотрудника."""


class IEmployeeInteractorResources(Protocol):
    """Контракт ресурсов (БД, сервисы) для сборки интеракторов (Employees)."""

    @property
    def session_factory(self) -> Callable[[], Any]:
        """Фабрика сессий. Возвращает объект сессии (AsyncSession) при вызове."""

    @property
    def token_service(self) -> ITokenService:
        """Сервис для работы с JWT или OAuth2 токенами."""

    @property
    def password_service(self) -> IPasswordService:
        """Сервис хеширования и проверки паролей."""

    @property
    def confirm_code_service(self) -> IConfirmationCodeService:
        """Генератор и верификатор кодов подтверждения (OTP)."""

    @property
    def email_service(self) -> IEmailService:
        """Транспорт для отправки уведомлений на почту."""

    @property
    def logger(self) -> ILogger:
        """Логгер."""
