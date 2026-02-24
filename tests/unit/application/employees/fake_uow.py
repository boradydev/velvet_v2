from copy import deepcopy

from src.domain.common.events import BaseDomainEvent
from src.domain.employees.entities import Employee


class FakeEmployeeRepository:
    def __init__(self):
        self.before_commit_employees = []
        self.after_commit_employees = []

    async def exists_by_email(self, email: str) -> bool:
        return any(e.email == email for e in self.before_commit_employees)

    async def save(self, employee: Employee) -> None:
        self.before_commit_employees.append(deepcopy(employee))
        self.after_commit_employees.append(employee)


class FakeEmployeeUOW:
    def __init__(self):
        self.employees = FakeEmployeeRepository()
        self.committed = False
        self.committed_events = []

    async def commit(self, events: list[BaseDomainEvent] | None = None):
        self.committed = True
        self.committed_events = events or []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass
