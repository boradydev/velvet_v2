from collections.abc import Mapping
from types import MappingProxyType

from src.core.exceptions import BaseAppException
from src.domain.employees.excs import (
    EmailNotFoundException,
    InvalidPasswordException,
)
from src.presentation.fastapi.common.types import Resp


EMPLOYEE_EXCEPTION_MAP: Mapping[type[BaseAppException], Resp] = MappingProxyType(
    {
        InvalidPasswordException: Resp(
            status_code=401,
            detail="Invalid credentials",
        ),
        EmailNotFoundException: Resp(
            status_code=401,
            detail="Invalid credentials",
        ),
    }
)


def get_swagger_exc(
    excs: tuple[type[BaseAppException], ...],
) -> dict[int, dict[str, str]]:
    responses: dict[int, dict[str, str]] = {}
    for exc in excs:
        key = EMPLOYEE_EXCEPTION_MAP.get(exc)
        if key:
            if key.status_code not in responses:
                responses[key.status_code] = {
                    "description": f"{key.detail}"}
            else:
                responses[key.status_code]["description"] += f" | {key.detail}"
        else:
            if 500 not in responses:
                responses[500] = {
                    "description": f"Unmapped exception: {exc.__name__}"}
            else:
                responses[500]["description"] += f" | {exc.__name__}"
    return responses
