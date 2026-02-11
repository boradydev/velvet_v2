from dataclasses import dataclass
from typing import Self

from uuid6 import UUID, uuid7

from src.domain.base.entities import BaseEntity
from src.domain.employees import value_objects
from src.domain.employees.exceptions import PermissionDeniedException


@dataclass(slots=True)
class Employee(BaseEntity):
    id: UUID
    email: value_objects.Email
    password_hash: value_objects.PasswordHash
    is_active: bool
    is_verified: bool
    role: value_objects.EmployeeRole
    permissions: set[str]

    def deactivate(self):
        self.is_active = False

    def verify(self):
        self.is_verified = True

    def promote_to_manager(self):
        self.role = value_objects.EmployeeRole.MANAGER

    def demote_to_saler(self):
        self.role = value_objects.EmployeeRole.SALER

    def has_permission(self, permission: value_objects.Permission) -> bool:
        if self.role == value_objects.EmployeeRole.OWNER:
            return True
        return permission in self.permissions

    def grant_permission(self, permission: value_objects.Permission):
        self.permissions.add(permission)

    def revoke_permission(self, permission: value_objects.Permission):
        if permission in self.permissions:
            self.permissions.remove(permission)

    def _ensure_can_perform(self, permission: value_objects.Permission):
        if self.role == value_objects.EmployeeRole.OWNER:
            return
        if permission not in self.permissions:
            raise PermissionDeniedException

    @classmethod
    def register(cls, email: str, password_hash: str) -> Self:
        """Фабричный метод, регистрация нового сотрудника."""
        return cls(
            id=uuid7(),
            email=value_objects.Email(email),
            password_hash=value_objects.PasswordHash(password_hash),
            is_active=True,
            is_verified=False,
            role=value_objects.EmployeeRole.SALER,
            permissions={
                value_objects.Permission.VIEW_PRODUCTS,
                value_objects.Permission.SALE,
                value_objects.Permission.SALE_RETURN,
            },
        )
