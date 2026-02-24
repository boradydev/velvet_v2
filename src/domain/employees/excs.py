from dataclasses import dataclass

from src.domain.common.exceptions import DomainException


@dataclass(frozen=True, slots=True)
class InvalidEmailException(DomainException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidPasswordHashException(DomainException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidPasswordException(DomainException):
    pass


@dataclass(frozen=True, slots=True)
class EmailNotFoundException(DomainException):
    pass


@dataclass(frozen=True, slots=True)
class PermissionDeniedException(DomainException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidRoleNameException(DomainException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidCredentialsException(DomainException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidConfirmationCodeException(DomainException):
    pass