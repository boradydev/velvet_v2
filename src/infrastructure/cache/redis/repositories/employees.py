from redis import Redis

from src.core.timezone import Timedelta
from src.domain.employees.interfaces.repos.cache_abc import IRegistrationRepository
from src.domain.employees.vals import ConfirmationCode, Email


class RedisRegistrationRepository(IRegistrationRepository):
    _KEY_PATTERN: str = "employee:auth:confirm_code:{email}"

    def __init__(self, client: Redis) -> None:
        self.client = client

    async def save_if_not_exists(
        self,
        email: Email,
        code: ConfirmationCode,
        ttl: Timedelta,
    ) -> None:
        key = self._KEY_PATTERN.format(email=email)
        await self.client.set(key, code, ex=ttl)

    async def save(
        self,
        email: Email,
        code: ConfirmationCode,
        ttl: Timedelta,
    ) -> None:
        key = self._KEY_PATTERN.format(email=email)
        await self.client.set(key, code, ex=ttl)

    async def get_by_email(self, email: Email) -> str | None:
        key = self._KEY_PATTERN.format(email=email)
        return await self.client.get(key)

    async def delete_by_email(self, email: Email) -> None:
        key = self._KEY_PATTERN.format(email=email)
        await self.client.delete(key)

    async def exists_by_email(self, *, email: Email) -> bool:
        raise NotImplementedError
