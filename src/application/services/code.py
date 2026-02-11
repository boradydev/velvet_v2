from typing import Protocol


class IConfirmationCodeService(Protocol):
    """Протокол генерации кодов подтверждения (OTP, email-tokens)."""

    def create_code(self) -> str:
        """Генерирует уникальный проверочный код."""
        ...
