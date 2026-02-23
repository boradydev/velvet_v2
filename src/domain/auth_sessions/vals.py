import ipaddress
from dataclasses import dataclass

from src.domain.auth_sessions import excs


@dataclass(frozen=True, slots=True)
class IpAddress:
    value: str

    def __post_init__(self):
        try:
            ipaddress.ip_address(self.value)
        except ValueError as exc:
            raise excs.InvalidIpAddressException from exc

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class UserAgent:
    value: str
    _MAX_LENGTH: int = 512

    def __post_init__(self):
        clean_value = self.value.strip()
        if not clean_value:
            raise excs.UserAgentIsEmptyException

        object.__setattr__(self, "value", clean_value[: self._MAX_LENGTH])

    def __str__(self) -> str:
        return self.value
