from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CredentialsEmployeeDTO:
    email: str
    password: str


@dataclass(frozen=True, slots=True)
class AccessTokenPayload:
    user_id: int
    role: str


@dataclass(frozen=True, slots=True)
class RefreshTokenPayload:
    session_id: int
