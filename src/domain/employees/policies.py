from abc import ABC, abstractmethod

from src.core.timezone import Timedelta


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
