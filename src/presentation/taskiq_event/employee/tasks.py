from typing import Annotated

from taskiq_dependencies import Depends

from src.application.employees.cases import (
    SendRegisterConfirmation,
)
from src.domain.employees.events import EmployeeRegisteredEvent
from src.domain.employees.vals import Email
from src.presentation.taskiq_event.app import broker
from src.presentation.taskiq_event.employee.dependencies import (
    get_send_code_confirmation,
)
from src.presentation.taskiq_event.employee.schemas import RegistrationTaskSchema


@broker.task(task_name="EmployeeRegisteredEvent")
async def handle_registration(
    payload: RegistrationTaskSchema,
    interactor: Annotated[
        SendRegisterConfirmation, Depends(get_send_code_confirmation)
    ],
):
    await interactor.execute(
        EmployeeRegisteredEvent(
            email=Email(payload.email),
            employee_id=payload.employee_id,
        )
    )
