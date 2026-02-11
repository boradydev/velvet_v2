from collections.abc import Mapping
from functools import cache
from types import MappingProxyType

from src.core.exceptions import BaseAppException
from src.domain.employees.exceptions import (
    EmailNotFoundException,
    InvalidPasswordException,
)
from src.presentation.fastapi.base.types import Resp


@cache
def EMPLOYEE_EXCEPTION_MAP_FUNC() -> Mapping[type[BaseAppException], Resp]:
    mappings: Mapping[type[BaseAppException], Resp] = {
        InvalidPasswordException: Resp(
            status_code=401,
            detail="Invalid credentials",
        ),
        EmailNotFoundException: Resp(
            status_code=401,
            detail="Invalid credentials",
        ),
    }
    return MappingProxyType(mappings)


EMPLOYEE_EXCEPTION_MAP_VAR: Mapping[type[BaseAppException], Resp] = MappingProxyType(
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
