from dataclasses import dataclass

from src.domain.base.exceptions import DomainException


@dataclass(frozen=True, slots=True)
class InvalidEmailException(DomainException): ...


@dataclass(frozen=True, slots=True)
class InvalidPasswordHashException(DomainException): ...

@dataclass(frozen=True, slots=True)
class InvalidPasswordException(DomainException): ...

@dataclass(frozen=True, slots=True)
class EmailNotFoundException(DomainException): ...

@dataclass(frozen=True, slots=True)
class PermissionDeniedException(DomainException): ...
