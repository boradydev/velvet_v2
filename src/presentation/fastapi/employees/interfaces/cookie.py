from abc import ABC, abstractmethod

from uuid6 import UUID


class IAuthCookieManager(ABC):
    @abstractmethod
    def set_auth_cookies(
        self,
        *,
        access_token: str,
        refresh_token: str,
        device_id: UUID,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_auth_cookies(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_device_id(self) -> str | None:
        raise NotImplementedError
