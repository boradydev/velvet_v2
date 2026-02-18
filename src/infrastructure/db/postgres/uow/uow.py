from collections.abc import Callable
from typing import Any, Self, cast

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.base.interfaces import IEventPublisher
from src.domain.employees.interfaces import IEmployeeRepository, IEmployeeUOW
from src.infrastructure.db.postgres.uow.base import IPostgresUOW


class EmployeeUOW(IPostgresUOW, IEmployeeUOW):
    """
    Реализация Unit of Work для управления транзакциями сущностей сотрудников.

    Attributes:
        _employee_repo_class: Класс для создания экземпляра репозитория.
        employees: Интерфейс доступа к коллекции сотрудников (репозиторий).
    """

    def __init__(
        self,
        session_factory: Callable[[], Any],
        employee_repo_class: Callable[[AsyncSession], IEmployeeRepository],
        event_publisher: IEventPublisher,
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
            employee_repo_class: Класс или фабрика для создания репозитория сотрудников.
        """
        self._session_factory = cast(async_sessionmaker[AsyncSession], session_factory)
        self._employee_repo_class = employee_repo_class
        self._event_publisher = event_publisher

    async def __aenter__(self) -> Self:
        """
        Инициализирует сессию и подготавливает репозитории к работе.

        Вызывается автоматически при входе в блок `async with`.
        """
        self._session = self._session_factory()
        self.employees = self._employee_repo_class(self._session)
        return self
