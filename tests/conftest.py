from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from faker import Faker

from src.application.common.interfaces import IEventPublisher
from src.application.employees.services import IEmployeeTasksService
from src.domain.common.interfaces import services_abc


@pytest.fixture
def mock_event_publisher() -> IEventPublisher | AsyncMock:
    return AsyncMock(spec_set=IEventPublisher)


@pytest.fixture
def mock_token_service() -> services_abc.ITokenService | AsyncMock:
    return AsyncMock(spec_set=services_abc.ITokenService)


@pytest.fixture
def mock_email_service() -> services_abc.IEmailService | AsyncMock:
    return AsyncMock(spec_set=services_abc.IEmailService)


@pytest.fixture
def mock_code_service() -> services_abc.IConfirmationCodeService | MagicMock:
    return MagicMock(spec_set=services_abc.IConfirmationCodeService)


@pytest.fixture
def mock_password_service() -> services_abc.IPasswordService | MagicMock:
    return MagicMock(spec_set=services_abc.IPasswordService)


@pytest.fixture
def mock_task_service() -> IEmployeeTasksService | MagicMock:
    return MagicMock(spec_set=IEmployeeTasksService)


@pytest.fixture
def mock_logger() -> services_abc.ILogger | MagicMock:
    return MagicMock(spec_set=services_abc.ILogger)


@pytest.fixture
def mock_now() -> MagicMock:
    """2026-01-01 12:00:00+00:00."""
    return MagicMock(return_value=datetime(2026, 1, 1, 12, 0, 0, tzinfo=UTC))


@pytest.fixture
def faker() -> Faker:
    return Faker()


