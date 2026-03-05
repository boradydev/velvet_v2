from dataclasses import dataclass

from src.core.exceptions import BaseAppException


@dataclass(frozen=True, slots=True)
class CookieNotFound(BaseAppException):
    pass
