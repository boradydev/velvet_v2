from src.domain.common.interfaces.services_abc import ITokenService
from src.infrastructure.auth.jwt.settings import JwtSettings


class JwtTokensService(ITokenService):
    _jwt_settings: JwtSettings

    def __init__(self, jwt_settings: JwtSettings) -> None:
        self._jwt_settings = jwt_settings
