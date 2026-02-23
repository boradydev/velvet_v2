from passlib.context import CryptContext

from src.domain.common.interfaces.services_abc import IPasswordService


class PasswordService(IPasswordService):
    _pwd_context: CryptContext

    def __init__(
        self,
        pwd_context: CryptContext,
    ) -> None:
        self._pwd_context = pwd_context

    def hashing_password(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)
