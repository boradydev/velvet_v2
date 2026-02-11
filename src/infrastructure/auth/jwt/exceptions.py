from dataclasses import dataclass

from src.core.exceptions import BaseAppException


@dataclass(frozen=True, slots=True)
class NotAnAccessTokenException(BaseAppException): ...


@dataclass(frozen=True, slots=True)
class NotARefreshTokenException(BaseAppException): ...


@dataclass(frozen=True, slots=True)
class ExpiredSignatureException(BaseAppException): ...


@dataclass(frozen=True, slots=True)
class InvalidSignatureException(BaseAppException): ...
