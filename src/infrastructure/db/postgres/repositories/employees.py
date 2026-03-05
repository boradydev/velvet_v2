from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.employees.interfaces.repos.db_abc import IEmployeeRepository


class EmployeeRepository(IEmployeeRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
