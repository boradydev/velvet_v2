import re
from typing import Annotated

from pydantic import AfterValidator, EmailStr, Field, SecretStr

from src.presentation.fastapi.common.schemas import BaseSchema
from src.presentation.fastapi.employees.exceptions import (
    ValidationPasswordHTTPException,
)


def validate_password_complexity(value: SecretStr) -> SecretStr:
    """
    Проверка пароля на соответствие требованиям сложности.

    Проверяет наличие как минимум одной заглавной буквы, одной строчной буквы,
    одной цифры и одного специального символа.
    """
    password_value = value.get_secret_value()

    rules = [
        (r"[A-Z]", "one uppercase letter"),
        (r"[a-z]", "one lowercase letter"),
        (r"[0-9]", "one digit"),
        (r'[!@#$%^&*(),.?":{}|<>]', "one special character"),
    ]

    for pattern, message in rules:
        if not re.search(pattern, password_value):
            raise ValidationPasswordHTTPException(
                detail=f"Password must contain at least {message}"
            )

    return value


class CredentialsRequest(BaseSchema):
    email: EmailStr
    password: Annotated[
        SecretStr,
        Field(
            min_length=8,
            max_length=50,
            examples=["Qwer123$"],
            description="От 8 до 50 символов: A-Z, a-z, 0-9 и спецсимволы.",
        ),
        AfterValidator(validate_password_complexity),
    ]


class ResendRequest(BaseSchema):
    email: EmailStr


class ConfirmRegisterRequest(BaseSchema):
    email: EmailStr
    confirm_code: str


class AuthTokensResponse(BaseSchema):
    access_token: str
    refresh_token: str
