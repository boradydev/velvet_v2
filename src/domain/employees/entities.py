from dataclasses import dataclass
from datetime import timedelta
from typing import Self

from uuid6 import UUID, uuid7

from src.core.timezone import Timedelta, Timestamp
from src.domain.auth_sessions.vals import IpAddress, UserAgent
from src.domain.common.entities import BaseEntity
from src.domain.employees import events, excs, vals


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
class Role(BaseEntity):
    id: UUID
    name: vals.RoleName
    is_system: bool
    _permissions: set[vals.PermissionName]

    @property
    def permissions(self) -> set[vals.PermissionName]:
        return self._permissions

    def add_permission(self, *, permission: vals.PermissionName) -> None:
        self._permissions.add(permission)

    def remove_permission(self, *, permission: vals.PermissionName) -> None:
        self._permissions.remove(permission)

    @classmethod
    def create(
        cls,
        *,
        name: vals.RoleName,
    ) -> Self:
        return cls(
            id=uuid7(),
            name=name,
            _permissions=set(),
            is_system=False,
        )


@dataclass(slots=True, kw_only=True)
class Employee(BaseEntity):
    id: UUID
    email: vals.Email
    _password_hash: vals.PasswordHash
    is_active: bool
    _roles_ids: set[UUID]
    _permission_names: set[vals.PermissionName]
    created_at: Timestamp

    def deactivate(self):
        self.is_active = False

    @property
    def password_hash(self) -> vals.PasswordHash:
        return self._password_hash

    @property
    def roles_ids(self) -> frozenset[UUID]:
        return frozenset(self._roles_ids)

    @property
    def permission_names(self) -> frozenset[vals.PermissionName]:
        return frozenset(self._permission_names)

    def add_role(self, *, role_id: UUID) -> None:
        self._roles_ids.add(role_id)

    @classmethod
    def create(
        cls,
        employee_id: UUID,
        email: vals.Email,
        password_hash: vals.PasswordHash,
        role_id: UUID,
        now: Timestamp,
    ) -> Self:
        employee = cls(
            id=employee_id,
            email=email,
            _password_hash=password_hash,
            is_active=True,
            _roles_ids={role_id},
            _permission_names=set(),
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
