from abc import ABC, abstractmethod
from typing import Protocol

from src.application.employees.dtos import (
    AccessTokenPayload,
    RefreshTokenPayload,
    SendConfirmationCodeDTO,
)
from src.domain.employees.vals import ConfirmationCode, Password, PasswordHash


class ILogger(Protocol):
    """Контракт для логгера."""

    def debug(self, msg, *args, **kwargs) -> None: ...
    def info(self, msg, *args, **kwargs) -> None: ...
    def error(self, msg, *args, **kwargs) -> None: ...
    def warning(self, msg, *args, **kwargs) -> None: ...
    def critical(self, msg, *args, **kwargs) -> None: ...
    def exception(self, msg, *args, **kwargs) -> None: ...


class IConfirmationCodeService(Protocol):
    """Протокол генерации кодов подтверждения (OTP, email-tokens)."""

    def generate(self) -> ConfirmationCode:
        """Генерирует уникальный проверочный код."""
        ...


class IPasswordService(ABC):
    """Интерфейс для безопасной работы с паролями пользователей."""

    @abstractmethod
    def hash(self, *, password: Password) -> PasswordHash:
        """Преобразует сырой пароль в безопасный хеш."""

    @abstractmethod
    def verify_password(
        self,
        *,
        plain_password: Password,
        hashed_password: PasswordHash,
    ) -> bool:
        """Проверяет соответствие сырого пароля ранее созданному хешу."""


class IEmailService(Protocol):
    async def send_confirmation_code(self, *, dto: SendConfirmationCodeDTO) -> None:
        """Отправляет сообщение."""


class ITokenService(ABC):
    @abstractmethod
    def create_access_token(self, **kwargs) -> str:
        """Создает токен доступа с полезной нагрузкой из переданных данных."""

    @abstractmethod
    def get_payload_access_token(self, access_token: str) -> AccessTokenPayload:
        """Возвращает payload токена доступа в виде dataclass."""

    @abstractmethod
    def create_refresh_token(self, **kwargs) -> str:
        """Создает токен обновления с полезной нагрузкой из переданных данных."""

    @abstractmethod
    def get_payload_refresh_token(self, refresh_token: str) -> RefreshTokenPayload:
        """Возвращает payload токена обновления в виде dataclass."""
