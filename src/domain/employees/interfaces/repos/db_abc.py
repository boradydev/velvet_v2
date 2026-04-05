from abc import ABC, abstractmethod

from uuid6 import UUID

from src.domain.auth_sessions.entity import AuthSession
from src.domain.employees.entities import Employee, Role
from src.domain.employees.vals import Email, RoleName


class IEmployeeRepository(ABC):
    """
    Интерфейс репозитория для управления данными сотрудников.

    Обеспечивает абстракцию над операциями доступа к данным,
    инкапсулируя логику поиска, сохранения и удаления сущностей сотрудников.
    """

    @abstractmethod
    async def add(self, *, employee: Employee) -> None:
        """
        Добавляет нового сотрудника в систему.

        Raises:
            EmployeeAlreadyExistsException: Если email или ID уже заняты.
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, *, employee: Employee) -> None:
        """Обновляет сотрудника в систему."""
        raise NotImplementedError

    @abstractmethod
    async def get_for_update_by_id(self, *, employee_id: UUID) -> Employee:
        """
        Использует пессимистичную блокировку.

        Raises:
            EmployeeNotFoundException: Если ID не существует.
        """
        raise NotImplementedError

    @abstractmethod
    async def exists_by_email(self, *, email: Email) -> bool:
        """Проверяет существование сотрудника по email."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(self, *, email: Email) -> Employee | None:
        """Поиск сотрудника по email."""
        raise NotImplementedError


class IAuthSessionsRepository(ABC):
    """Интерфейс репозитория для управления сессиями аутентификации."""

    @abstractmethod
    async def save(self, *, auth_session: AuthSession) -> None:
        """Сохраняет новую сессию или обновляет существующую."""
        raise NotImplementedError

    @abstractmethod
    async def get(
        self,
        *,
        auth_session_id: UUID,
        employee_id: UUID,
    ) -> AuthSession:
        """
        Получает сессию аутентификации по id и employee_id.

        Raises:
            AuthSessionNotFoundException: Если не найдена.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *, auth_session: AuthSession) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_for_update(
        self,
        *,
        device_id: UUID,
        employee_id: UUID,
    ) -> AuthSession | None:
        """Использует пессимистичную блокировку."""
        raise NotImplementedError


class IRolesRepository(ABC):
    """Интерфейс репозитория для управления ролями сотрудника."""

    @abstractmethod
    async def get_by_name(self, *, role_name: RoleName) -> Role:
        """
        Получить роль по имени.

        Raises:
            RoleNotFoundException
        """
        raise NotImplementedError
