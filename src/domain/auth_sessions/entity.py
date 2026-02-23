from dataclasses import dataclass
from typing import Self

from uuid6 import UUID, uuid7

from src.core.timezone import Timedelta, Timestamp, get_timestamp
from src.domain.auth_sessions import events, excs, vals
from src.domain.common.entities import BaseEntity


@dataclass(slots=True, kw_only=True)
class AuthSession(BaseEntity):
    id: UUID
    employee_id: UUID
    device_id: UUID
    expires_at: Timestamp
    created_at: Timestamp
    _refresh_token: str | None
    user_agent: vals.UserAgent | None
    ip_address: vals.IpAddress | None

    def is_expired(self) -> bool:
        return get_timestamp() > self.expires_at

    @classmethod
    def create(
        cls,
        *,
        employee_id: UUID,
        expires_delta: Timedelta,
        refresh_token: str | None = None,
        device_id: UUID | None = None,
        user_agent: vals.UserAgent | None = None,
        ip_address: vals.IpAddress | None = None,
    ) -> Self:
        auth_session = cls(
            id=uuid7(),
            employee_id=employee_id,
            device_id=device_id or uuid7(),
            _refresh_token=refresh_token,
            user_agent=user_agent,
            ip_address=ip_address,
            expires_at=get_timestamp() + expires_delta,
            created_at=get_timestamp(),
        )
        if not device_id:
            auth_session._add_event(
                events.NewDeviceSessionCreatedEvent(
                    auth_session_id=auth_session.id,
                    device_id=auth_session.device_id,
                    employee_id=employee_id,
                )
            )

        return auth_session

    def save_refresh_token(self, refresh_token: str):
        self._refresh_token = refresh_token

    @property
    def refresh_token(self) -> str:
        if not self._refresh_token:
            raise excs.RefreshTokenNotFoundException
        return self._refresh_token
