from abc import ABC, abstractmethod

from src.application.employees.dtos import ConfirmationEmployeeDTO
from src.domain.employees.vals import Email


class IConfirmationCodeRepository(ABC):
    @abstractmethod
    async def save(
        self,
        email: Email,
        dto: ConfirmationEmployeeDTO,
        ttl: int,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_email(self, email: Email) -> ConfirmationEmployeeDTO | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, email: Email) -> None:
        raise NotImplementedError
