from dataclasses import dataclass
from typing import Self

from uuid6 import UUID

from src.core.timezone import Timestamp
from src.domain.auth_sessions import events, excs, vals
from src.domain.common.entities import BaseEntity


@dataclass(slots=True, kw_only=True)
class AuthSession(BaseEntity):
    id: UUID
    employee_id: UUID
    user_agen: vals.UserAgent
    ip_address: vals.IpAddress | None
    expires_at: Timestamp
    created_at: Timestamp
    _refresh_token_hash: vals.RefreshTokenHash

    @property
    def refresh_token_hash(self) -> vals.RefreshTokenHash:
        return self._refresh_token_hash

    @classmethod
    def create(
        cls,
        *,
        session_id: UUID,
        employee_id: UUID,
        user_agent: vals.UserAgent,
        ip_address: vals.IpAddress | None,
        refresh_token_hash: vals.RefreshTokenHash,
        now: Timestamp,
        expires_at: Timestamp,
    ) -> Self:
        auth_session = cls(
            id=session_id,
            employee_id=employee_id,
            _refresh_token_hash=refresh_token_hash,
            user_agen=user_agent,
            ip_address=ip_address,
            created_at=now,
            expires_at=expires_at,
        )
        auth_session._add_event(
            events.NewDeviceSessionCreatedEvent(
                auth_session_id=auth_session.id,
                user_agent=auth_session.user_agen,
                employee_id=employee_id,
                created_at=now,
            )
        )
        return auth_session

    def is_expired(self, now: Timestamp) -> bool:
        return now > self.expires_at

    def rotate(
        self,
        *,
        requested_by: UUID,
        new_hash: vals.RefreshTokenHash,
        expires_at: Timestamp,
        now: Timestamp,
    ) -> None:
        self.ensure_ownership(requested_by=requested_by)
        if self.is_expired(now):
            raise excs.InvalidRefreshTokenException

        self._refresh_token_hash = new_hash
        self.expires_at = expires_at
        self._add_event(
            event=events.SessionRotated(
                auth_session_id=self.id,
                created_at=now,
            )
        )

    def ensure_ownership(self, *, requested_by: UUID) -> None:
        if self.employee_id != requested_by:
            raise excs.SessionOwnershipViolationException

    def close(
        self,
        *,
        requested_by: UUID,
        now: Timestamp,
    ) -> None:
        self.ensure_ownership(requested_by=requested_by)
        self._add_event(
            event=events.AuthSessionDeleted(
                auth_session_id=self.id,
                created_at=now,
            )
        )

    def flag_theft_attempt(
        self,
        *,
        requested_by: UUID,
        now: Timestamp,
    ):
        self._add_event(
            event=events.AuthSessionTheftAttempted(
                auth_session_id=self.id,
                requested_by=requested_by,
                created_at=now,
            )
        )
        self.close(
            requested_by=self.employee_id,
            now=now,
        )
