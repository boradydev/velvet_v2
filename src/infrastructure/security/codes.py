import secrets


class ConfirmCodeService:
    def create_code(self) -> str:
        """Создаёт новый код подтверждения."""
        return f"{secrets.randbelow(1_000_000):06}"
