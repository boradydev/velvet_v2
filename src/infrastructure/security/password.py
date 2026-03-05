from passlib.context import CryptContext

from src.domain.common.interfaces.services_abc import IPasswordService
from src.domain.employees.vals import Password, PasswordHash


class PasswordService(IPasswordService):
    _pwd_context: CryptContext

    def __init__(
        self,
        pwd_context: CryptContext,
    ) -> None:
        self._pwd_context = pwd_context

    def hash(self, *, password: Password) -> PasswordHash:
        return PasswordHash(self._pwd_context.hash(password.value))

    def verify_password(
        self,
        *,
        plain_password: Password,
        hashed_password: PasswordHash,
    ) -> bool:
        return self._pwd_context.verify(plain_password.value, hashed_password.value)
