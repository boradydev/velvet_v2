from dataclasses import dataclass

from src.core.exceptions import VelvetException


@dataclass(frozen=True, slots=True)
class NotAnAccessTokenException(VelvetException): ...


@dataclass(frozen=True, slots=True)
class NotARefreshTokenException(VelvetException): ...


@dataclass(frozen=True, slots=True)
class ExpiredSignatureException(VelvetException): ...


@dataclass(frozen=True, slots=True)
class InvalidSignatureException(VelvetException): ...
