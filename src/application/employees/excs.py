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
