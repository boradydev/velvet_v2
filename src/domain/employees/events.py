from dataclasses import dataclass

from uuid6 import UUID

from src.domain.common.events import BaseDomainEvent
from src.domain.employees import vals


@dataclass(frozen=True, slots=True, kw_only=True)
class EmployeeRegisteredEvent(BaseDomainEvent):
    employee_id: UUID
    email: vals.Email


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationEvent(BaseDomainEvent):
    email: vals.Email
    confirmation_code: vals.ConfirmationCode


@dataclass(frozen=True, slots=True, kw_only=True)
class ConfirmationCodeResentEvent(BaseDomainEvent):
    email: vals.Email
    confirmation_code: vals.ConfirmationCode


@dataclass(frozen=True, slots=True, kw_only=True)
class RegistrationConfirmedEvent(BaseDomainEvent):
    email: vals.Email
