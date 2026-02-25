from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from tests.unit.application.employees.fake_uow import (
    FakeConfirmationCodeRepository,
    FakeEmployeeUOW,
)


@pytest.fixture
def employee_uow() -> FakeEmployeeUOW:
    return FakeEmployeeUOW()


@pytest.fixture
def fake_confirmation_code_repo() -> FakeConfirmationCodeRepository:
    return FakeConfirmationCodeRepository()


@pytest.fixture
def fake_email_service() -> AsyncMock:
    return AsyncMock()


@pytest.fixture
def fake_code_service() -> MagicMock:
    return MagicMock()


@pytest.fixture
def fake_logger() -> MagicMock:
    return MagicMock()


@pytest.fixture
def frozen_now():
    """2026-01-01 12:00:00+00:00."""
    return datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def get_now_mock(frozen_now):
    """2026-01-01 12:00:00+00:00."""
    return lambda: frozen_now
