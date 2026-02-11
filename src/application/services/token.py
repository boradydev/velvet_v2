from abc import ABC, abstractmethod

from src.application.employees.dto import AccessTokenPayload, RefreshTokenPayload


class ITokenService(ABC):
    @abstractmethod
    def create_access_token(self, **kwargs) -> str:
        """Создает токен доступа из переданных данных."""

    @abstractmethod
    def get_payload_access_token(self, access_token: str) -> AccessTokenPayload:
        """Возвращает payload токена доступа в виде dataclass."""

    @abstractmethod
    def create_refresh_token(self, **kwargs) -> str:
        """Создает токен обновления из переданных данных."""

    @abstractmethod
    def get_payload_refresh_token(self, refresh_token: str) -> RefreshTokenPayload:
        """Возвращает payload токена обновления в виде dataclass."""
