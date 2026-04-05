from collections.abc import Sequence

from sqlalchemy import delete, exists, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from src.application.employees.excs import (
    EmployeeAlreadyExistsException,
    EmployeeNotFoundException,
)
from src.domain.employees.entities import Employee
from src.domain.employees.interfaces.repos.db_abc import IEmployeeRepository
from src.domain.employees.vals import Email, PasswordHash, PermissionName
from src.infrastructure.db.postgres.models.employees import (
    EmployeeORM,
    EmployeeRoleORM,
    RolePermissionORM,
)


class EmployeeRepository(IEmployeeRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, *, employee: Employee) -> None:
        try:
            self.session.add(
                EmployeeORM(
                    id=employee.id,
                    email=str(employee.email),
                    password_hash=str(employee.password_hash),
                    is_active=employee.is_active,
                    created_at=employee.created_at,
                )
            )
            self.session.add_all(
                [
                    EmployeeRoleORM(
                        employee_id=employee.id,
                        role_id=role_id,
                    )
                    for role_id in employee.roles_ids
                ]
            )
            await self.session.flush()
        except IntegrityError as exc:
            raise EmployeeAlreadyExistsException from exc

    async def get_for_update_by_id(self, *, employee_id: UUID) -> Employee:
        employee_fetch = await self.session.execute(
            select(EmployeeORM).where(EmployeeORM.id == employee_id).with_for_update()
        )
        employee_orm: EmployeeORM | None = employee_fetch.scalars().one_or_none()
        if not employee_orm:
            raise EmployeeNotFoundException

        role_ids_fetch = await self.session.execute(
            select(EmployeeRoleORM.role_id)
            .where(EmployeeRoleORM.employee_id == employee_id)
            .with_for_update()
        )
        role_ids: Sequence[UUID] = role_ids_fetch.scalars().all()

        permissions_fetch = await self.session.execute(
            select(RolePermissionORM.permission_name).where(
                RolePermissionORM.role_id.in_(role_ids)
            )
        )
        permission_names: Sequence[str] = permissions_fetch.scalars().all()

        return Employee(
            id=employee_orm.id,
            email=Email(employee_orm.email),
            _password_hash=PasswordHash(employee_orm.password_hash),
            is_active=employee_orm.is_active,
            created_at=employee_orm.created_at,
            _roles_ids={role_id for role_id in role_ids},
            _permission_names={
                PermissionName(permission_name) for permission_name in permission_names
            },
        )

    async def update(self, *, employee: Employee) -> None:
        await self.session.execute(
            update(EmployeeORM)
            .where(EmployeeORM.id == employee.id)
            .values(
                email=str(employee.email),
                password_hash=str(employee.password_hash),
                is_active=employee.is_active,
            )
        )
        await self.session.execute(
            delete(EmployeeRoleORM).where(EmployeeRoleORM.employee_id == employee.id)
        )
        self.session.add_all(
            [
                EmployeeRoleORM(
                    employee_id=employee.id,
                    role_id=role_id,
                )
                for role_id in employee.roles_ids
            ]
        )

    async def exists_by_email(self, *, email: Email) -> bool:
        result = await self.session.execute(
            select(exists().where(EmployeeORM.email == str(email)))
        )
        return bool(result.scalar())

    async def find_by_email(self, *, email: Email) -> Employee | None:
        employee_fetch = await self.session.execute(
            select(EmployeeORM).where(EmployeeORM.email == str(email)).with_for_update()
        )
        employee_orm: EmployeeORM | None = employee_fetch.scalars().one_or_none()
        if not employee_orm:
            return None

        role_ids_fetch = await self.session.execute(
            select(EmployeeRoleORM.role_id)
            .where(EmployeeRoleORM.employee_id == employee_orm.id)
            .with_for_update()
        )
        role_ids: Sequence[UUID] = role_ids_fetch.scalars().all()

        permissions_fetch = await self.session.execute(
            select(RolePermissionORM.permission_name).where(
                RolePermissionORM.role_id.in_(role_ids)
            )
        )
        permission_names: Sequence[str] = permissions_fetch.scalars().all()

        return Employee(
            id=employee_orm.id,
            email=Email(employee_orm.email),
            _password_hash=PasswordHash(employee_orm.password_hash),
            is_active=employee_orm.is_active,
            created_at=employee_orm.created_at,
            _roles_ids={role_id for role_id in role_ids},
            _permission_names={
                PermissionName(permission_name) for permission_name in permission_names
            },
        )
