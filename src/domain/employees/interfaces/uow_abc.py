from abc import ABC, abstractmethod

from src.domain.common.interfaces.uow_abc import InterfaceUOW
from src.domain.employees.interfaces.repos import db_abc


class IEmployeeUOW(InterfaceUOW, ABC):
    """Интерфейс Unit of Work для управления транзакциями данных сотрудников."""

    @property
    @abstractmethod
    def employees(self) -> db_abc.IEmployeeRepository:
        """Требует репозиторий для сотрудников."""
        raise NotImplementedError

    @property
    @abstractmethod
    def auth_sessions(self) -> db_abc.IAuthSessionsRepository:
        """Требует репозиторий для сессий аутентификации."""
        raise NotImplementedError
