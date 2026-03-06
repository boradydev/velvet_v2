from dataclasses import dataclass

from uuid6 import UUID

from src.domain.auth_sessions.vals import IpAddress, RefreshToken, UserAgent
from src.domain.employees import vals


@dataclass(frozen=True, slots=True, kw_only=True)
class CredentialsEmployeeDTO:
    email: vals.Email
    password: vals.Password
    user_agent: UserAgent
    ip_address: IpAddress


@dataclass(frozen=True, slots=True, kw_only=True)
class ConfirmRegisterDTO:
    email: vals.Email
    confirmation_code: vals.ConfirmationCode
    user_agent: UserAgent
    ip_address: IpAddress


@dataclass(frozen=True, slots=True, kw_only=True)
class AccessTokenPayload:
    user_id: UUID
    role: vals.RoleName


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshTokenPayload:
    auth_session_id: UUID
    employee_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class SendConfirmationCodeDTO:
    email: vals.Email
    confirmation_code: vals.ConfirmationCode


@dataclass(frozen=True, slots=True, kw_only=True)
class ResendConfirmationCodeDTO:
    email: vals.Email
    ip_address: IpAddress


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthTokensDTO:
    access_token: str
    refresh_token: str


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshDTO:
    refresh_token: RefreshToken
    user_agent: UserAgent
    ip_address: IpAddress


@dataclass(frozen=True, slots=True, kw_only=True)
class LogoutDTO:
    refresh_token: RefreshToken
