from dataclasses import dataclass

from uuid6 import UUID

from src.domain.base.events import BaseDomainEvent


@dataclass(frozen=True, slots=True)
class EmployeeRegisteredEvent(BaseDomainEvent):
    employee_id: UUID
    email: str
