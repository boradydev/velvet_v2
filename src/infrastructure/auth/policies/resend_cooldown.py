from datetime import timedelta

from src.core.timezone import Timedelta
from src.domain.employees.interfaces.policies import IRegistrationPolicy


class ExponentialBackoffPolicy(IRegistrationPolicy):
    def get_cooldown(self, resend_count: int) -> Timedelta:
        seconds = min(60 * (2**resend_count), 3600)
        return timedelta(seconds=seconds)
