from src.application.employees.dto import ResendCodeEmployeeDTO
from src.infrastructure.tasks.task_iq import tasks


class TaskIQEmployeeTasksService:
    """Реализация сервиса уведомлений через TaskIQ (RabbitMQ)."""

    async def task_resend_by_email(self, dto: ResendCodeEmployeeDTO) -> None:
        await tasks.employees.task_resend_by_email.kiq(dto)
