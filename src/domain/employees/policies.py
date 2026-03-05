from abc import ABC, abstractmethod

from src.core.timezone import Timedelta, Timestamp
from src.domain.employees.vals import RoleName


class IRegistrationPolicy(ABC):
    @abstractmethod
    def get_confirmation_ttl(self) -> Timedelta:
        """Возвращает общее время жизни подтверждения."""
        raise NotImplementedError

    @abstractmethod
    def get_cooldown(self, *, resend_count: int) -> Timedelta:
        """Возвращает время паузы перед возможностью повторной отправки кода."""
        raise NotImplementedError

    @abstractmethod
    def get_min_resend_ttl(self) -> Timedelta:
        """Возвращает минимальный остаток, при котором еще разрешена переотправка."""
        raise NotImplementedError

    def get_default_role(self) -> RoleName:
        """Возвращает роль сотрудника, которая назначается по умолчанию."""
        raise NotImplementedError

    def get_refresh_session_expires_at(self, *, now: Timestamp) -> Timestamp:
        """Возвращает время истечения сессии аутентификации и токена обновления."""
        raise NotImplementedError

    def get_access_expires_at(self, *, now: Timestamp) -> Timestamp:
        """Возвращает время истечения токена доступа."""
        raise NotImplementedError
