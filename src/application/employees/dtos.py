from dataclasses import dataclass

from uuid6 import UUID

from src.core.timezone import Timestamp
from src.domain.employees import vals


@dataclass(frozen=True, slots=True, kw_only=True)
class CredentialsEmployeeDTO:
    email: vals.Email
    password: vals.Password


@dataclass(frozen=True, slots=True, kw_only=True)
class LoginCredentialsEmployeeDTO:
    email: vals.Email
    password: vals.Password
    device_id: UUID | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ConfirmRegisterDTO:
    email: vals.Email
    confirmation_code: vals.ConfirmationCode


@dataclass(frozen=True, slots=True, kw_only=True)
class AccessTokenPayload:
    user_id: int
    role: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshTokenPayload:
    session_id: int


@dataclass(frozen=True, slots=True, kw_only=True)
class SendConfirmationCodeDTO:
    email: vals.Email
    confirmation_code: vals.ConfirmationCode


@dataclass(frozen=True, slots=True, kw_only=True)
class ResendConfirmationCodeDTO:
    email: vals.Email


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthTokensDTO:
    access_token: str
    refresh_token: str
    device_id: UUID
