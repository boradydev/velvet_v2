from collections.abc import Mapping
from types import MappingProxyType

from src.core.exceptions import BaseAppException
from src.domain.employees.exceptions import (
    EmailNotFoundException,
    InvalidPasswordException,
)
from src.presentation.fastapi.base.types import Resp


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
