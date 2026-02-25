from copy import deepcopy
from dataclasses import dataclass

from uuid6 import UUID

from src.application.employees.dtos import ConfirmationEmployeeDTO
from src.domain.common.events import BaseDomainEvent
from src.domain.employees.entities import Employee
from src.domain.employees.interfaces.repos.cache_abc import IConfirmationCodeRepository
from src.domain.employees.interfaces.repos.db_abc import IEmployeeRepository
from src.domain.employees.interfaces.uow_abc import IEmployeeUOW
from src.domain.employees.vals import Email


class FakeEmployeeRepository(IEmployeeRepository):
    def __init__(self):
        self.before_commit_employees = []
        self.after_commit_employees = []

    async def exists_by_email(self, email: Email) -> bool:
        return any(e.email == email for e in self.before_commit_employees)

    async def save(self, employee: Employee) -> None:
        self.before_commit_employees.append(deepcopy(employee))
        self.after_commit_employees.append(employee)

    async def get_by_id(self, employee_id: UUID) -> Employee | None:
        raise NotImplementedError

    async def delete_by_id(self, employee_id: UUID) -> None:
        raise NotImplementedError

    async def get_id_by_email(self, email: Email) -> UUID | None:
        raise NotImplementedError

    async def get_by_email(self, email) -> Employee | None:
        raise NotImplementedError


class FakeEmployeeUOW(IEmployeeUOW):
    employees: FakeEmployeeRepository

    def __init__(self):
        self.employees = FakeEmployeeRepository()  # type: ignore
        self.committed = False
        self.committed_events = []

    async def commit(self, events: list[BaseDomainEvent] | None = None):
        self.committed = True
        self.committed_events = events or []

    async def rollback(self) -> None:
        raise NotImplementedError

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


@dataclass
class StorageEntry:
    dto: ConfirmationEmployeeDTO
    ttl: int


class FakeConfirmationCodeRepository(IConfirmationCodeRepository):
    def __init__(self):
        self.storage: dict[Email, StorageEntry] = {}

    async def save(
        self,
        email: Email,
        dto: ConfirmationEmployeeDTO,
        ttl: int,
    ) -> None:
        self.storage[email] = StorageEntry(dto=deepcopy(dto), ttl=ttl)

    async def get_by_email(self, email: Email) -> ConfirmationEmployeeDTO | None:
        entry = self.storage.get(email)
        return entry.dto if entry else None

    async def delete(self, email: Email) -> None:
        raise NotImplementedError
