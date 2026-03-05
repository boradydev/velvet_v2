from dataclasses import dataclass
from typing import Self

from uuid6 import UUID, uuid7

from src.core.timezone import Timestamp
from src.domain.common.entities import BaseEntity
from src.domain.employees.vals import Permission


@dataclass(slots=True, kw_only=True)
class Role(BaseEntity):
    id: UUID
    name: str
    permissions: set[Permission]
    created_at: Timestamp

    def add_permission(self, *, permission: Permission) -> None:
        self.permissions.add(permission)

    def remove_permission(self, *, permission: Permission) -> None:
        self.permissions.remove(permission)

    @classmethod
    def create_role(
        cls,
        *,
        name: str,
        timestamp: Timestamp,
    ) -> Self:
        return cls(
            id=uuid7(),
            name=name,
            permissions=set(),
            created_at=timestamp,
        )
