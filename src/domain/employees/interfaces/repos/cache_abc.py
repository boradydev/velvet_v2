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
        raise NotImplementedError

    @abstractmethod
    async def save(
        self,
        *,
        email: Email,
        dto: Registration,
        ttl: Timedelta,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, *, email: Email) -> Registration | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_email(self, *, email: Email) -> None:
        raise NotImplementedError

    @abstractmethod
    async def exists_by_email(self, *, email: Email) -> bool:
        raise NotImplementedError
