from dataclasses import dataclass
from datetime import timedelta
from typing import Self

from uuid6 import UUID

from src.core.timezone import Timedelta, Timestamp
from src.domain.auth_sessions.vals import IpAddress, UserAgent
from src.domain.common.entities import BaseEntity
from src.domain.employees import events, excs, vals
from src.domain.employees.excs import PermissionDeniedException


@dataclass(slots=True, kw_only=True)
class Registration(BaseEntity):
    email: vals.Email
    password_hash: vals.PasswordHash
    user_agent: UserAgent
    ip_address: IpAddress | None
    confirmation_code: vals.ConfirmationCode
    resend_count: int
    last_code_sent_at: Timestamp
    confirmation_deadline: Timestamp
    version: int

    def time_left(self, *, now: Timestamp) -> Timedelta:
        return max(timedelta(0), self.confirmation_deadline - now)

    def has_enough_time_left(
        self,
        *,
        now: Timestamp,
        min_ttl: Timedelta,
    ) -> bool:
        return self.time_left(now=now) >= min_ttl

    def can_resend(
        self,
        *,
        now: Timestamp,
        cooldown: Timedelta,
    ) -> bool:
        return now >= self.last_code_sent_at + cooldown

    def resend(
        self,
        *,
        new_code: vals.ConfirmationCode,
        now: Timestamp,
    ):
        self.confirmation_code = new_code
        self.resend_count += 1
        self.last_code_sent_at = now
        self.version += 1
        self._add_event(
            event=events.ConfirmationCodeResentEvent(
                email=self.email,
                confirmation_code=self.confirmation_code,
                created_at=now,
            )
        )

    def is_expired(self, *, now: Timestamp) -> bool:
        return now > self.confirmation_deadline

    def confirm(
        self,
        *,
        code: vals.ConfirmationCode,
        now: Timestamp,
    ) -> None:
        if self.is_expired(now=now):
            raise excs.RegistrationExpired

        if self.confirmation_code != code:
            raise excs.InvalidConfirmationCode

        self._add_event(
            events.RegistrationConfirmedEvent(
                email=self.email,
                created_at=now,
            )
        )

    @classmethod
    def create(
        cls,
        *,
        email: vals.Email,
        password_hash: vals.PasswordHash,
        user_agent: UserAgent,
        ip_address: IpAddress | None,
        confirmation_code: vals.ConfirmationCode,
        confirmation_ttl: Timedelta,
        now: Timestamp,
    ) -> Self:
        registration = cls(
            email=email,
            password_hash=password_hash,
            user_agent=user_agent,
            ip_address=ip_address,
            confirmation_code=confirmation_code,
            resend_count=0,
            last_code_sent_at=now,
            confirmation_deadline=now + confirmation_ttl,
            version=1,
        )
        registration._add_event(
            events.RegistrationEvent(
                email=registration.email,
                confirmation_code=registration.confirmation_code,
                created_at=now,
            )
        )
        return registration


@dataclass(slots=True, kw_only=True)
class Employee(BaseEntity):
    id: UUID
    email: vals.Email
    _password_hash: vals.PasswordHash
    is_active: bool
    has_roles: set[vals.RoleName]
    available_roles: set[vals.RoleName]
    permissions: set[vals.Permission]
    created_at: Timestamp

    def deactivate(self):
        self.is_active = False

    @property
    def password_hash(self) -> vals.PasswordHash:
        return self._password_hash

    @property
    def is_owner(self) -> bool:
        return vals.SystemRoles.OWNER.value in self.has_roles

    def add_role(self, *, role: vals.RoleName) -> None:
        if not (self.is_owner or vals.Permission.MANAGE_ROLES in self.permissions):
            raise PermissionDeniedException
        self.available_roles.add(role)

    def has_permission(self, *, permission: vals.Permission) -> bool:
        if self.is_owner:
            return True
        return permission in self.permissions

    def _ensure_can_perform(self, *, permission: vals.Permission):
        if self.is_owner:
            return
        if permission not in self.permissions:
            raise PermissionDeniedException

    @classmethod
    def create(
        cls,
        employee_id: UUID,
        email: vals.Email,
        password_hash: vals.PasswordHash,
        role: vals.RoleName,
        now: Timestamp,
    ) -> Self:
        employee = cls(
            id=employee_id,
            email=email,
            _password_hash=password_hash,
            is_active=True,
            has_roles={role},
            available_roles=set(),
            permissions=set(),
            created_at=now,
        )
        employee._add_event(
            events.EmployeeRegisteredEvent(
                employee_id=employee.id,
                email=employee.email,
                created_at=now,
            )
        )
        return employee
