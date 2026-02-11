from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from uuid6 import UUID

from src.domain.employees.entities import Employee


class IEmployeeRepository(ABC):
    """
    Интерфейс репозитория для управления данными сотрудников.

    Обеспечивает абстракцию над операциями доступа к данным,
    инкапсулируя логику поиска, сохранения и удаления сущностей сотрудников.
    """

    @abstractmethod
    async def add(self, employee: Employee) -> None:
        """Добавляет нового сотрудника в систему."""

    @abstractmethod
    async def get_by_id(self, employee_id: UUID) -> Employee | None:
        """Восстанавливает состояние агрегата сотрудника по его идентификатору."""

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        """Проверяет, зарегистрирован ли уже сотрудник с таким email."""

    @abstractmethod
    async def update(self, employee: Employee) -> None:
        """Сохраняет измененное состояние существующего сотрудника."""

    @abstractmethod
    async def delete(self, employee_id: UUID) -> None:
        """Удаляет сотрудника и связанные с ним данные из системы."""


class IPasswordService(ABC):
    """Интерфейс для безопасной работы с паролями пользователей."""

    @abstractmethod
    def hashing_password(self, password: str) -> str:
        """Преобразует сырой пароль в безопасный хеш."""

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверяет соответствие сырого пароля ранее созданному хешу."""


class IEmployeeUOW(ABC):
    """
    Интерфейс Unit of Work для управления транзакциями данных сотрудников.

    Обеспечивает атомарность операций (ACID).
    """

    employees: IEmployeeRepository

    @abstractmethod
    async def __aenter__(self) -> Self:
        """Открывает транзакцию и подготавливает ресурсы."""

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Закрывает контекст. Выполняет автоматический откат при ошибке."""

    @abstractmethod
    async def commit(self) -> None:
        """Фиксирует все изменения текущей транзакции в базе данных."""

    @abstractmethod
    async def rollback(self) -> None:
        """Отменяет все незафиксированные изменения."""
