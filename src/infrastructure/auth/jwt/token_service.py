import secrets
from datetime import timedelta, datetime, timezone
from typing import Any

import jwt
from passlib.context import CryptContext

from src.infrastructure.auth.jwt.exceptions import (
    NotAnAccessTokenException,
    NotARefreshTokenException,
    ExpiredSignatureException,
    InvalidSignatureException,
)

from src.infrastructure.auth.jwt.settings import jwt_settings


class TokensService:
    _pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)

    def create_access_token(self, **kwargs) -> str:
        """
        Создаёт JWT access-токен с заданными данными и временем истечения.

        Аргументы:
            **kwargs: Ключевые аргументы (payload), которые нужно закодировать в токене.

        Возвращает:
            str: Сформированный JWT access-токен в виде строки.

        Примечания:
            - В токен автоматически добавляется поле "exp" (время истечения),
              на основе настроек `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`.
            - Секрет и алгоритм берутся из конфигурации (`jwt_settings.JWT_SECRET_KEY`, `jwt_settings.JWT_ALGORITHM`).
        """
        to_encode = kwargs.copy()
        expires_delta = timedelta(minutes=jwt_settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire, "type_token": "access"})
        encoded_jwt = jwt.encode(
            to_encode,
            jwt_settings.JWT_SECRET_KEY.get_secret_value(),
            algorithm=jwt_settings.JWT_ALGORITHM,
        )
        return str(encoded_jwt)

    def create_refresh_token(self, **kwargs) -> str:
        """
        Генерирует JWT refresh-токен с истечением срока и заданными данными.

        Аргументы:
            **kwargs: Ключевые аргументы (payload), которые нужно закодировать в токене.

        Возвращает:
            str: Сформированный JWT refresh-токен в виде строки.

        Примечания:
            - В токен автоматически добавляется поле "exp" (время истечения),
              на основе настроек `JWT_REFRESH_TOKEN_EXPIRE_DAYS`.
            - Секрет и алгоритм берутся из конфигурации (`jwt_settings.JWT_SECRET_KEY`, `jwt_settings.JWT_ALGORITHM`).
        """
        to_encode = kwargs.copy()
        expires_delta = timedelta(days=jwt_settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire, "type_token": "refresh"})
        encoded_jwt = jwt.encode(
            to_encode,
            jwt_settings.JWT_SECRET_KEY.get_secret_value(),
            algorithm=jwt_settings.JWT_ALGORITHM,
        )
        return str(encoded_jwt)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет соответствие введённого пароля и хэша.

        Аргументы:
            plain_password (str): Обычный (не захешированный) пароль.
            hashed_password (str): Хэш пароля, сохранённый в базе данных.

        Возвращает:
            bool: True, если пароль совпадает с хэшем, иначе False.
        """
        return self._pwd_context.verify(plain_password, hashed_password)

    def decode_access_token(self, access_token: str) -> dict[str, Any]:
        """
        Декодирует access-токен и проверяет его тип.

        Аргументы:
            access_token (str): JWT access-токен.

        Возвращает:
            dict: Payload токена.

        Исключения:
            NotAnAccessTokenException: Если тип токена не 'access'.
            jwt.ExpiredSignatureError: Если срок действия токена истёк.
            jwt.InvalidSignatureError: Если подпись токена недействительна.
        """
        payload = self._jwt_decode(token=access_token)
        if payload["type_token"] != "access":
            raise NotAnAccessTokenException
        return payload

    def decode_refresh_token(self, refresh_token: str) -> dict[str, Any]:
        """
        Декодирует refresh-токен и проверяет его тип.

        Аргументы:
            refresh_token (str): JWT refresh-токен.

        Возвращает:
            dict: Payload токена.

        Исключения:
            NotARefreshTokenException: Если тип токена не 'refresh'.
            jwt.ExpiredSignatureError: Если срок действия токена истёк.
            jwt.InvalidSignatureError: Если подпись токена недействительна.
        """
        payload = self._jwt_decode(token=refresh_token)
        if payload["type_token"] != "refresh":
            raise NotARefreshTokenException
        return payload

    def _jwt_decode(self, token: str) -> dict[str, Any]:
        """
        Декодирует JWT-токен без проверки его типа.

        Аргументы:
            token (str): JWT-токен (access или refresh).

        Возвращает:
            dict: Расшифрованный payload токена.

        Исключения:
            jwt.ExpiredSignatureError: Если срок действия токена истёк.
            jwt.InvalidSignatureError: Если подпись токена недействительна.
        """
        try:
            payload: dict[str, Any] = jwt.decode(
                token,
                jwt_settings.JWT_SECRET_KEY.get_secret_value(),
                algorithms=[jwt_settings.JWT_ALGORITHM],
            )
        except jwt.ExpiredSignatureError as exc:
            raise ExpiredSignatureException from exc
        except jwt.InvalidSignatureError as exc:
            raise InvalidSignatureException from exc
        except Exception as exc:
            raise exc
        return payload

    @staticmethod
    def create_confirm_code() -> str:
        return f"{secrets.randbelow(1_000_000):06}"


token_service = TokensService()
