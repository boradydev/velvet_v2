from typing import Annotated

from taskiq_dependencies import Depends

from src.application.employees.cases import SendConfirmation
from src.infrastructure.common.resources import AppState
from src.presentation.fastapi.common.common_deps import get_app_state


def get_send_code_confirmation(
    resources: Annotated[AppState, Depends(get_app_state)],
) -> SendConfirmation:
    return resources.cases.employees.create_send_registration_confirmation()
