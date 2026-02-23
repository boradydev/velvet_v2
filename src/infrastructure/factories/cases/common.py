from collections.abc import Callable
from typing import Any

from src.application.base.interfaces import IEventPublisher
from src.application.employees.interfaces import IEmployeeUseCaseFactory
from src.domain.common.interfaces.services_abc import (
    IConfirmationCodeService,
    IEmailService,
    ILogger,
    IPasswordService,
    ITokenService,
)
from src.infrastructure.factories.cases.employees import EmployeeUseCaseFactory


class UseCaseResources:
    """Корень композиции (Composition Root)."""

    def __init__(
        self,
        session_factory: Callable[[], Any],
        token_service: ITokenService,
        password_service: IPasswordService,
        confirm_code_service: IConfirmationCodeService,
        email_service: IEmailService,
        logger: ILogger,
        event_publisher: IEventPublisher,
    ) -> None:
        self._session_factory = session_factory
        self._token_service = token_service
        self._password_service = password_service
        self._confirm_code_service = confirm_code_service
        self._email_service = email_service
        self._logger = logger
        self._event_publisher = event_publisher

        self.employees: IEmployeeUseCaseFactory = EmployeeUseCaseFactory(self)

    @property
    def session_factory(self) -> Callable[[], Any]:
        return self._session_factory

    @property
    def token_service(self) -> ITokenService:
        return self._token_service

    @property
    def password_service(self) -> IPasswordService:
        return self._password_service

    @property
    def confirm_code_service(self) -> IConfirmationCodeService:
        return self._confirm_code_service

    @property
    def email_service(self) -> IEmailService:
        return self._email_service

    @property
    def even_bus(self) -> IEventPublisher:
        return self._event_publisher

    @property
    def logger(self) -> ILogger:
        return self._logger
