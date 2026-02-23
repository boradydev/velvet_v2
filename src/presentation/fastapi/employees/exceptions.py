from src.presentation.fastapi.common import exceptions


class ValidationPasswordHTTPException(exceptions.ValidationHTTPException):
    """Ожидает аргумент detail для описания ошибки пароля."""

class InvalidCredentialsHTTPException(exceptions.UnauthorizedHTTPException):
    detail = "Invalid credentials"