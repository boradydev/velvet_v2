from src.application.employees.dtos import ResendConfirmationCodeDTO
from src.infrastructure.tasks.task_iq.tasks.broker import tasks_broker


@tasks_broker.task
async def task_resend_by_email(dto: ResendConfirmationCodeDTO) -> None:
    """Создает задачу отправки кода подтверждения по почте."""


