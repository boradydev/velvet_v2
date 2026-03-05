from src.application.employees import dtos
from src.core.timezone import Timestamp
from src.domain.auth_sessions.vals import RefreshTokenHash
from src.domain.common.interfaces.services_abc import ITokenService
from src.infrastructure.auth.jwt.settings import JwtSettings


class JwtTokensService(ITokenService):
    _jwt_settings: JwtSettings

    def __init__(self, *, settings: JwtSettings) -> None:
        self._jwt_settings = settings

    def create_access_token(
        self,
        *,
        expires_at: Timestamp,
        **kwargs,
    ) -> str:
        """Создает токен доступа с полезной нагрузкой из переданных данных."""
        raise NotImplementedError

    def get_payload_access_token(
        self,
        *,
        access_token: str,
    ) -> dtos.AccessTokenPayload:
        """Возвращает payload токена доступа в виде dataclass."""
        raise NotImplementedError

    def create_refresh_token(
        self,
        *,
        expires_at: Timestamp,
        **kwargs,
    ) -> str:
        """Создает токен обновления с полезной нагрузкой из переданных данных."""
        raise NotImplementedError

    def get_payload_refresh_token(
        self,
        *,
        refresh_token: str,
    ) -> dtos.RefreshTokenPayload:
        """Возвращает payload токена обновления в виде dataclass."""
        raise NotImplementedError

    def hash_refresh_token(
        self,
        *,
        refresh_token: str,
    ) -> RefreshTokenHash:
        """Возвращает хэш токена обновления."""
        raise NotImplementedError

    def verify_hash_refresh_token(
        self,
        *,
        plain_token: str,
        hashed_token: RefreshTokenHash,
    ) -> bool:
        """Проверяет, что токен обновления соответствует хэшу."""
        raise NotImplementedError
