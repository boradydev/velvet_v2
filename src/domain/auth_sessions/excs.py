from dataclasses import dataclass

from src.domain.common.exceptions import DomainException


@dataclass(frozen=True, slots=True)
class RefreshTokenNotFoundException(DomainException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidIpAddressException(DomainException):
    pass


@dataclass(frozen=True, slots=True)
class UserAgentIsEmptyException(DomainException):
    pass