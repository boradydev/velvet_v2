from redis import Redis

from src.domain.employees.interfaces.repos.cache_abc import IRegistrationRepository


class RedisRegistrationRepository(IRegistrationRepository):
    """
    Репозиторий временного хранилища регистрации сотрудника.

    Attributes:
        _KEY_PATTERN: Использование: key = self._KEY_PATTERN.format(email=email).
    """

    _KEY_PATTERN: str = "employee:auth:confirm_code:{email}"

    def __init__(self, client: Redis) -> None:
        self.client = client
