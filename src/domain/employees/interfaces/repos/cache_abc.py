from abc import ABC, abstractmethod

from src.core.timezone import Timedelta
from src.domain.employees.entities import Registration
from src.domain.employees.vals import Email


class IRegistrationRepository(ABC):
    @abstractmethod
    async def save_if_not_exists(
        self,
        *,
        email: Email,
        dto: Registration,
        ttl: Timedelta,
    ) -> None:
        """Сохраняет, если еще не существует."""
        raise NotImplementedError

    @abstractmethod
    async def save_if_version_matches(
        self,
        *,
        email: Email,
        dto: Registration,
        ttl: Timedelta,
    ) -> None:
        """Сохраняет, если существует и версия совпадает (Оптимистичная блокировка)."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_email(self, *, email: Email) -> Registration | None:
        """Получает по емэил."""
        raise NotImplementedError

    @abstractmethod
    async def delete_by_email(self, *, email: Email) -> None:
        """Удаляет по емэил."""
        raise NotImplementedError

    @abstractmethod
    async def exists_by_email(self, *, email: Email) -> bool:
        """Проверяет существование по емэил."""
        raise NotImplementedError
