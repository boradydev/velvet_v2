from src.application.employees.dto import ResendCodeEmployeeDTO
from src.infrastructure.tasks.task_iq.tasks.broker import tasks_broker


@tasks_broker.task
async def task_resend_by_email(dto: ResendCodeEmployeeDTO) -> None:
    """Создает задачу отправки кода подтверждения по почте."""


