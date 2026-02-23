from redis import Redis

from src.domain.employees.interfaces.repos.cache_abc import IConfirmationCodeRepository


class RedisConfirmationCodeRepository(IConfirmationCodeRepository):
    _KEY_PATTERN: str = "employee:auth:confirm_code:{email}"

    def __init__(self, client: Redis) -> None:
        self.client = client

    async def save(
        self,
        email: str,
        code: str,
        ttl: int,
    ) -> None:
        key = self._KEY_PATTERN.format(email=email)
        await self.client.set(key, code, ex=ttl)

    async def get_by_email(self, email: str) -> str | None:
        key = self._KEY_PATTERN.format(email=email)
        return await self.client.get(key)

    async def delete(self, email: str) -> None:
        key = self._KEY_PATTERN.format(email=email)
        await self.client.delete(key)
