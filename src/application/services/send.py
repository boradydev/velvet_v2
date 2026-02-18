from typing import Protocol

from src.domain.employees.value_objects import Email


class IEmailService(Protocol):
    async def send(self, email: Email, message: str):
        """Отправляет сообщение."""
