from dataclasses import dataclass

from uuid6 import UUID

from src.application.employees.excs import ConfirmationCodeActiveException
from src.core.timezone import Timestamp
from src.domain.employees.vals import ConfirmationCode, Email


@dataclass(frozen=True, slots=True, kw_only=True)
class CredentialsEmployeeDTO:
    email: Email
    password: str


@dataclass(frozen=True, slots=True, kw_only=True)
class LoginCredentialsEmployeeDTO:
    email: Email
    password: str
    device_id: UUID | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ConfirmRegisterDTO:
    email: Email
    confirmation_code: ConfirmationCode


@dataclass(frozen=True, slots=True, kw_only=True)
class AccessTokenPayload:
    user_id: int
    role: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshTokenPayload:
    session_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class SendConfirmationDTO:
    employee_id: UUID
    email: Email


@dataclass(frozen=True, slots=True, kw_only=True)
class ConfirmationEmployeeDTO:
    employee_id: UUID
    email: Email
    code: ConfirmationCode
    cooldown: Timestamp


@dataclass(frozen=True, slots=True, kw_only=True)
class ResendCodeEmployeeDTO:
    email: Email


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthTokensDTO:
    access_token: str
    refresh_token: str
    device_id: UUID