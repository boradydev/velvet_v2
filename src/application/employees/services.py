from typing import Protocol

from src.application.employees import dtos


class IEmployeeTasksService(Protocol):
    async def send_by_email(self, dto: dtos.SendConfirmationDTO):
        """Создает задачу отправки кода подтверждения по почте."""
        ...
