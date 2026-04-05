from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domain.employees import excs
from src.domain.employees.entities import Role
from src.domain.employees.interfaces.repos.db_abc import IRolesRepository
from src.domain.employees.vals import PermissionName, RoleName
from src.infrastructure.db.postgres.models.employees import RoleORM


class RolesRepository(IRolesRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_name(self, *, role_name: RoleName) -> Role:
        result = await self.session.execute(
            select(RoleORM)
            .options(selectinload(RoleORM.permissions))
            .where(RoleORM.name == role_name)
        )
        role_orm: RoleORM | None = result.scalars().one_or_none()

        if not role_orm:
            raise excs.RoleNotFoundException

        return Role(
            id=role_orm.id,
            name=RoleName(role_orm.name),
            is_system=role_orm.is_system,
            _permissions={
                PermissionName(permission.name) for permission in role_orm.permissions
            },
        )
