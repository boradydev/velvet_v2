from datetime import UTC, datetime


def get_now() -> datetime:
    """Глобальный провайдер времени UTC."""
    return datetime.now(UTC)
