from collections.abc import Callable
from typing import Any, Self, cast

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.common.interfaces import IEventPublisher
from src.domain.employees.interfaces.repos import db_abc
from src.domain.employees.interfaces.uow_abc import IEmployeeUOW
from src.infrastructure.db.postgres.uow.common import IPostgresUOW


class EmployeeUOW(IPostgresUOW, IEmployeeUOW):
    """
    Реализация Unit of Work для управления транзакциями сущностей сотрудников.

    Attributes:
        _employee_class: Класс для создания экземпляра репозитория.
        _employees: Интерфейс доступа к коллекции сотрудников (репозиторий).
    """

    def __init__(
        self,
        session_factory: Callable[[], Any],
        event_publisher: IEventPublisher,
        employee_class: Callable[[AsyncSession], db_abc.IEmployeeRepository],
        auth_session_class: Callable[[AsyncSession], db_abc.IAuthSessionsRepository],
    ) -> None:
        """
        Инициализирует Unit of Work.

        Этот класс является точкой сопряжения абстрактного интерфейса IEmployeeUOW
            и конкретной реализации БД через SQLAlchemy.
        Принимает абстрактную фабрику сессий и приводит её к конкретной
        реализации SQLAlchemy (async_sessionmaker) для обеспечения
        строгой типизации в рамках инфраструктурного слоя PostgreSQL.

        Args:
            session_factory: Абстрактный поставщик сессий (Callable).
            event_publisher: Абстрактный поставщик брокера событий.
            employee_class: Класс или фабрика для создания репозитория сотрудников.
            auth_session_class: Класс или фабрика для создания репозитория
                сессий аутентификации.
        """
        self._session_factory = cast(async_sessionmaker[AsyncSession], session_factory)
        self._event_publisher = event_publisher
        self._employee_class = employee_class
        self._auth_sessions_class = auth_session_class

    async def __aenter__(self) -> Self:
        """
        Инициализирует сессию и подготавливает репозитории к работе.

        Вызывается автоматически при входе в блок `async with`.
        """
        self._session = self._session_factory()
        self._employees = self._employee_class(self._session)
        self._auth_sessions = self._auth_sessions_class(self._session)
        return self

    @property
    def employees(self) -> db_abc.IEmployeeRepository:
        return self._employees

    @property
    def auth_sessions(self) -> db_abc.IAuthSessionsRepository:
        return self._auth_sessions
