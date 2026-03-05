from typing import Annotated

from taskiq_dependencies import Depends

from src.application.employees import cases, dtos
from src.domain.employees.vals import ConfirmationCode, Email
from src.presentation.taskiq_event.app import broker
from src.presentation.taskiq_event.employee import deps, schemas


@broker.task(task_name="EmployeeRegisteredEvent")
async def handle_registration(
    payload: schemas.RegistrationTaskSchema,
    case: Annotated[cases.SendConfirmation, Depends(deps.get_send_code_confirmation)],
) -> None:
    await case.execute(
        dto=dtos.SendConfirmationCodeDTO(
            email=Email(payload.email),
            confirmation_code=ConfirmationCode(payload.confirmation_code),
        )
    )
