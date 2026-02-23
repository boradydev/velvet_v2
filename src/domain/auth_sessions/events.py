from dataclasses import dataclass

from uuid6 import UUID

from src.domain.common.events import BaseDomainEvent
from src.domain.employees.vals import Email


@dataclass(frozen=True, slots=True, kw_only=True)
class EmployeeRegisteredEvent(BaseDomainEvent):
    employee_id: UUID
    email: Email

@dataclass(frozen=True, slots=True, kw_only=True)
class NewDeviceSessionCreatedEvent(BaseDomainEvent):
    auth_session_id: UUID
    device_id: UUID
    employee_id: UUID