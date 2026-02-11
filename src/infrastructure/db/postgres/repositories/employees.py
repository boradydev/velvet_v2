from sqlalchemy.ext.asyncio import AsyncSession
from uuid6 import UUID

from src.domain.employees.entities import Employee
from src.domain.employees.interfaces import IEmployeeRepository


class EmployeeRepository(IEmployeeRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, employee: Employee) -> None:
        """Сохраняет новый агрегат Employee в базу."""

    async def get_by_id(self, employee_id: UUID) -> Employee:
        """Восстанавливает агрегат Employee из базы по ID."""

    async def exists_by_email(self, email: str) -> bool:
        """Находит сотрудника по email (для проверок при регистрации)."""

    async def update(self, employee: Employee) -> None:
        """Обновляет агрегат в базе данных Employee в базу."""

    async def delete(self, employee_id: UUID) -> None:
        """Удаляет агрегат."""
