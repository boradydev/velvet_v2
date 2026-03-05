import secrets

from src.domain.employees.vals import ConfirmationCode


class ConfirmCodeService:
    def generate(self) -> ConfirmationCode:
        """Создаёт новый код подтверждения."""
        return ConfirmationCode(f"{secrets.randbelow(1_000_000):06}")
