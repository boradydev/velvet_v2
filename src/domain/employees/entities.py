from dataclasses import dataclass
from typing import Self

from uuid6 import UUID, uuid7

from src.core.timezone import Timestamp
from src.domain.common.entities import BaseEntity
from src.domain.common.interfaces.services_abc import IPasswordService
from src.domain.employees import excs
from src.domain.employees.events import EmployeeRegisteredEvent
from src.domain.employees.excs import PermissionDeniedException
from src.domain.employees.vals import (
    Email,
    PasswordHash,
    Permission,
    RoleName,
    SystemRoles,
)


@dataclass(slots=True, kw_only=True)
class Employee(BaseEntity):
    id: UUID
    email: Email
    _password_hash: PasswordHash
    is_active: bool
    is_verified: bool
    has_roles: set[RoleName]
    available_roles: set[RoleName]
    permissions: set[Permission]
    created_at: Timestamp

    def deactivate(self):
        self.is_active = False

    def verify(self):
        self.is_verified = True

    def check_password(
        self,
        password: str,
        password_service: IPasswordService,
    ) -> bool:
        if not password_service.verify_password(password, self._password_hash.value):
            raise excs.InvalidCredentialsException
        return True

    @property
    def is_owner(self) -> bool:
        return SystemRoles.OWNER in self.has_roles

    def add_role(self, role: RoleName) -> None:
        if not (self.is_owner or Permission.MANAGE_ROLES in self.permissions):
            raise PermissionDeniedException
        self.available_roles.add(role)

    def has_permission(self, permission: Permission) -> bool:
        if self.is_owner:
            return True
        return permission in self.permissions

    def _ensure_can_perform(self, permission: Permission):
        if self.is_owner:
            return
        if permission not in self.permissions:
            raise PermissionDeniedException

    @classmethod
    def register(
        cls,
        email: Email,
        password_hash: str,
        timestamp: Timestamp,
    ) -> Self:
        """Фабричный метод, регистрация нового сотрудника."""
        employee = cls(
            id=uuid7(),
            email=email,
            _password_hash=PasswordHash(password_hash),
            is_active=True,
            is_verified=False,
            has_roles=set(),
            available_roles=set(),
            permissions=set(),
            created_at=timestamp,
        )
        employee._add_event(
            EmployeeRegisteredEvent(
                employee_id=employee.id,
                email=employee.email,
                timestamp=timestamp,
            )
        )
        return employee
