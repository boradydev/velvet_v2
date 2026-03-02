import ipaddress
import re
from dataclasses import dataclass, field
from typing import ClassVar, Final

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


@dataclass(frozen=True, slots=True)
class RefreshTokenHash:
    """
    Хранимый хэш Refresh-токена.

    Гарантирует, что строка является валидным результатом SHA-256 (hex-представление).
    ``^[a-f0-9]`` - только шестнадцатеричные символы в нижнем регистре

    ``{64}`` - строго 64 символа (длина SHA-256 в hex)
    """

    value: str = field(repr=False)

    _PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^[a-f0-9]{64}$")

    def __post_init__(self) -> None:
        has_pattern = self._PATTERN.match(self.value)

        if not has_pattern:
            raise excs.InvalidRefreshTokenHashException
