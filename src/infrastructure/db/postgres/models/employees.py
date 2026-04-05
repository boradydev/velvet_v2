from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid6 import UUID

from src.core.timezone import Timestamp
from src.infrastructure.db.postgres.models.common import BaseModel


class PermissionORM(BaseModel):
    __tablename__ = "permissions"
    name: Mapped[str] = mapped_column(primary_key=True)


class RolePermissionORM(BaseModel):
    __tablename__ = "role_permissions"
    permission_name: Mapped[str] = mapped_column(
        ForeignKey(column="permissions.name", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="roles.id", ondelete="CASCADE"),
        primary_key=True,
    )


class RoleORM(BaseModel):
    __tablename__ = "roles"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    is_system: Mapped[bool] = mapped_column()

    permissions: Mapped[set[PermissionORM]] = relationship(
        secondary="role_permissions",
        collection_class=set,
    )


class EmployeeRoleORM(BaseModel):
    __tablename__ = "employee_roles"
    employee_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="employees.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey(column="roles.id", ondelete="CASCADE"),
        primary_key=True,
    )


class EmployeeORM(BaseModel):
    __tablename__ = "employees"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    created_at: Mapped[Timestamp] = mapped_column()
