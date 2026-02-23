from abc import ABC, abstractmethod

from uuid6 import UUID

from src.domain.auth_sessions.entitity import AuthSession
from src.domain.employees.entities import Employee
from src.domain.employees.vals import Email


class IEmployeeRepository(ABC):
    """
    Интерфейс репозитория для управления данными сотрудников.

    Обеспечивает абстракцию над операциями доступа к данным,
    инкапсулируя логику поиска, сохранения и удаления сущностей сотрудников.
    """

    @abstractmethod
    async def save(self, employee: Employee) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, employee_id: UUID) -> Employee | None:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, employee_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_id_by_email(self, email: Email) -> UUID | None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email) -> Employee | None:
        raise NotImplementedError


class IAuthSessionsRepository(ABC):
    """Интерфейс репозитория для управления сессиями аутентификации."""

    @abstractmethod
    async def save(self, auth_session: AuthSession) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, auth_session_id: UUID) -> AuthSession | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, auth_session_id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_device_and_employee_id(
        self, device_id: UUID, employee_id: UUID
    ) -> AuthSession | None:
        raise NotImplementedError
