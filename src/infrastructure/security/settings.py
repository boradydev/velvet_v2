from dataclasses import dataclass

from passlib.context import CryptContext


@dataclass(frozen=True, slots=True)
class PasswordSettings:
    DEFAULT_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
