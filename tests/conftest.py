from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain.common.interfaces import services_abc
from src.domain.employees.interfaces.repos import db_abc
from src.domain.employees.interfaces.uow_abc import IEmployeeUOW
from tests.unit.application.employees import fakes


@pytest.fixture
def fake_employee_uow() -> fakes.FakeEmployeeUOW:
    return fakes.FakeEmployeeUOW()


@pytest.fixture
def mock_employee_uow() -> IEmployeeUOW | AsyncMock:
    uow = AsyncMock(spec_set=IEmployeeUOW)
    uow.employees = AsyncMock(spec_set=db_abc.IEmployeeRepository)
    uow.auth_sessions = AsyncMock(spec_set=db_abc.IAuthSessionsRepository)
    return uow


@pytest.fixture
def fake_confirmation_code_repo() -> fakes.FakeConfirmationCodeRepository:
    return fakes.FakeConfirmationCodeRepository()


@pytest.fixture
def mock_email_service() -> services_abc.IEmailService | AsyncMock:
    return AsyncMock(spec_set=services_abc.IEmailService)


@pytest.fixture
def mock_code_service() -> services_abc.IConfirmationCodeService | MagicMock:
    return MagicMock(spec_set=services_abc.IConfirmationCodeService)


@pytest.fixture
def mock_pass_service() -> services_abc.IPasswordService | MagicMock:
    return MagicMock(spec_set=services_abc.IPasswordService)


@pytest.fixture
def mock_logger() -> services_abc.ILogger | MagicMock:
    return MagicMock(spec_set=services_abc.ILogger)


@pytest.fixture
def frozen_now():
    """2026-01-01 12:00:00+00:00."""
    return datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC)


@pytest.fixture
def mock_get_now(frozen_now):
    """2026-01-01 12:00:00+00:00."""

    def get_frozen_now():
        return frozen_now

    return get_frozen_now
