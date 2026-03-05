from dataclasses import dataclass

from uuid6 import UUID

from src.core.timezone import Timestamp
from src.domain.auth_sessions.vals import UserAgent
from src.domain.common.events import BaseDomainEvent
from src.domain.employees.vals import Email


@dataclass(frozen=True, slots=True, kw_only=True)
class EmployeeRegisteredEvent(BaseDomainEvent):
    employee_id: UUID
    email: Email


@dataclass(frozen=True, slots=True, kw_only=True)
class NewDeviceSessionCreatedEvent(BaseDomainEvent):
    auth_session_id: UUID
    user_agent: UserAgent
    employee_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class SessionRotated(BaseDomainEvent):
    auth_session_id: UUID
    created_at: Timestamp


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthSessionDeleted(BaseDomainEvent):
    auth_session_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthSessionTheftAttempted(BaseDomainEvent):
    auth_session_id: UUID
    requested_by: UUID
