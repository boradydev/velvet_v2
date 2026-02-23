from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

from src.application.employees.dtos import AccessTokenPayload, RefreshTokenPayload
from src.domain.common.interfaces.services_abc import ITokenService
from src.infrastructure.auth.jwt import exceptions
from src.infrastructure.auth.jwt.settings import JwtSettings


class JwtTokensService(ITokenService):
    _jwt_settings: JwtSettings

    def __init__(self, jwt_settings: JwtSettings) -> None:
        self._jwt_settings = jwt_settings

    def create_access_token(self, **kwargs) -> str:
        """
        Создаёт JWT access-токен с заданными данными и временем истечения.

        В токен автоматически добавляется поле "exp" (время истечения),
            на основе настроек `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.
        Секрет и алгоритм берутся из конфигурации
            (`self._jwt_settings.JWT_SECRET_KEY`, `self._jwt_settings.JWT_ALGORITHM`).

        Args:
            **kwargs: Ключевые аргументы (payload), которые нужно закодировать в токене.

        Returns:
            str: Сформированный JWT access-токен в виде строки.
        """
        to_encode = kwargs.copy()
        expires_delta = timedelta(
            minutes=self._jwt_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        expire = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire, "type_token": "access"})
        encoded_jwt = jwt.encode(
            to_encode,
            self._jwt_settings.JWT_SECRET_KEY,
            algorithm=self._jwt_settings.JWT_ALGORITHM,
        )
        return str(encoded_jwt)

    def create_refresh_token(self, **kwargs) -> str:
        """
        Генерирует JWT refresh-токен с истечением срока и заданными данными.

        Args:
            **kwargs: Ключевые аргументы (payload), которые нужно закодировать в токене.

        Returns:
            str: Сформированный JWT refresh-токен в виде строки.

        Raises:
            - В токен автоматически добавляется поле "exp" (время истечения),
              на основе настроек `JWT_REFRESH_TOKEN_EXPIRE_DAYS`.
            - Секрет и алгоритм берутся из конфигурации
            (`self._jwt_settings.JWT_SECRET_KEY`, `self._jwt_settings.JWT_ALGORITHM`).
        """
        to_encode = kwargs.copy()
        expires_delta = timedelta(days=self._jwt_settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        expire = datetime.now(UTC) + expires_delta
        to_encode.update({"exp": expire, "type_token": "refresh"})
        encoded_jwt = jwt.encode(
            to_encode,
            self._jwt_settings.JWT_SECRET_KEY,
            algorithm=self._jwt_settings.JWT_ALGORITHM,
        )
        return str(encoded_jwt)

    def get_payload_access_token(self, access_token: str) -> AccessTokenPayload:
        """
        Декодирует access-токен и проверяет его тип.

        Args:
            access_token (str): JWT access-токен.

        Returns:
            dict: Payload токена.

        Raises:
            NotAnAccessTokenException: Если тип токена не "access".
            jwt.ExpiredSignatureError: Если срок действия токена истёк.
            jwt.InvalidSignatureError: Если подпись токена недействительна.
        """
        payload = self._jwt_decode(token=access_token)
        if payload["type_token"] != "access":
            raise exceptions.NotAnAccessTokenException
        return AccessTokenPayload(**payload)

    def get_payload_refresh_token(self, refresh_token: str) -> RefreshTokenPayload:
        """
        Декодирует refresh-токен и проверяет его тип.

        Аргументы:
            refresh_token (str): JWT refresh-токен.

        Returns:
            dict: Payload токена.

        Raises:
            NotARefreshTokenException: Если тип токена не "refresh".
            jwt.ExpiredSignatureError: Если срок действия токена истёк.
            jwt.InvalidSignatureError: Если подпись токена недействительна.
        """
        payload = self._jwt_decode(token=refresh_token)
        if payload["type_token"] != "refresh":
            raise exceptions.NotARefreshTokenException
        return RefreshTokenPayload(**payload)

    def _jwt_decode(self, token: str) -> dict[str, Any]:
        """
        Декодирует JWT-токен без проверки его типа.

        Args:
            token (str): JWT-токен (access или refresh).

        Returns:
            dict: Расшифрованный payload токена.

        Raises:
            jwt.ExpiredSignatureError: Если срок действия токена истёк.
            jwt.InvalidSignatureError: Если подпись токена недействительна.
        """
        try:
            return jwt.decode(
                token,
                self._jwt_settings.JWT_SECRET_KEY,
                algorithms=[self._jwt_settings.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError as exc:
            raise exceptions.ExpiredSignatureException from exc
        except jwt.InvalidSignatureError as exc:
            raise exceptions.InvalidSignatureException from exc
