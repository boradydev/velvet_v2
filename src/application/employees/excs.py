from dataclasses import dataclass

from src.core.exceptions import BaseAppException


@dataclass(frozen=True, slots=True)
class EmployeeAlreadyExistsException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class EmployeeNotFoundException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class ConfirmationCodeActiveException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class ConfirmationCodeNotFoundException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class EmailDeliveryException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidConfirmationCodeException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class InvalidCredentialsEmployeeException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class RegistrationAlreadyExistsException(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class RegistrationNotFound(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class CooldownNotExpired(BaseAppException):
    pass


@dataclass(frozen=True, slots=True)
class TooLateToResend(BaseAppException):
    pass
