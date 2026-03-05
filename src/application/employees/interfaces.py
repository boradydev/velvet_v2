from collections.abc import Callable
from typing import Any, Protocol

from src.application.common.interfaces import IEventPublisher
from src.application.employees import cases
from src.core.timezone import Timestamp
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
    def session_factory(self) -> Callable[[], Any]: ...

    @property
    def token_service(self) -> ITokenService: ...

    @property
    def password_service(self) -> IPasswordService: ...

    @property
    def event_publisher(self) -> IEventPublisher: ...

    @property
    def logger(self) -> ILogger: ...

    @property
    def get_now(self) -> Callable[[], Timestamp]: ...
