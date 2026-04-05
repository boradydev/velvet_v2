from collections.abc import Callable
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.employees import dtos
from src.application.employees.cases import (
    ConfirmRegister,
    Register,
    ReSendCodeConfirmation,
)
from src.domain.auth_sessions.vals import UserAgent
from src.domain.employees.entities import Registration
from src.domain.employees.interfaces.repos import db_abc
from src.domain.employees.interfaces.repos.cache_abc import IRegistrationRepository
from src.domain.employees.interfaces.uow_abc import IEmployeeUOW
from src.domain.employees.interfaces.policies import IRegistrationPolicy
from src.domain.employees.vals import ConfirmationCode, Email, Password, PasswordHash


@pytest.fixture
def mock_employee_uow() -> IEmployeeUOW | AsyncMock:
    uow = AsyncMock(spec_set=IEmployeeUOW)
    uow.employees = AsyncMock(spec_set=db_abc.IEmployeeRepository)
    uow.auth_sessions = AsyncMock(spec_set=db_abc.IAuthSessionsRepository)
    return uow


@pytest.fixture
def mock_registration_repo() -> IRegistrationRepository | AsyncMock:
    return AsyncMock(spec_set=IRegistrationRepository)


@pytest.fixture
def mock_registration_policy() -> IRegistrationPolicy | MagicMock:
    return MagicMock(spec_set=IRegistrationPolicy)


@pytest.fixture
def use_case_register(
    mock_employee_uow,
    mock_registration_repo,
    mock_event_publisher,
    mock_password_service,
    mock_code_service,
    mock_now,
    mock_registration_policy,
) -> Register:
    return Register(
        uow=mock_employee_uow,
        registration_repo=mock_registration_repo,
        event_publisher=mock_event_publisher,
        password_service=mock_password_service,
        code_service=mock_code_service,
        get_now=mock_now,
        policy=mock_registration_policy,
    )


@pytest.fixture
def use_case_confirm_register(
    mock_employee_uow,
    mock_registration_repo,
    mock_token_service,
    mock_now,
    mock_id_generator,
    mock_registration_policy,
) -> ConfirmRegister:
    return ConfirmRegister(
        uow=mock_employee_uow,
        registration_repo=mock_registration_repo,
        token_service=mock_token_service,
        get_now=mock_now,
        id_generator=mock_id_generator,
        auth_policy=mock_registration_policy,
    )


@pytest.fixture
def creds_employee_dto(
    password,
    email,
) -> dtos.CredentialsEmployeeDTO:
    return dtos.CredentialsEmployeeDTO(
        email=email,
        password=password,
        user_agent=UserAgent("test_user_agent"),
    )


@pytest.fixture
def confirmation_registration_dto(
    email,
    confirmation_code,
) -> dtos.ConfirmRegisterDTO:
    return dtos.ConfirmRegisterDTO(
        email=email,
        confirmation_code=confirmation_code,
    )


@pytest.fixture
def confirmation_code(faker) -> ConfirmationCode:
    return ConfirmationCode(faker.bothify(text="######"))


@pytest.fixture
def resend_confirmation_code_dto(email) -> dtos.ResendConfirmationCodeDTO:
    return dtos.ResendConfirmationCodeDTO(email=email)


@pytest.fixture
def resend_use_case(
    mock_registration_repo,
    mock_event_publisher,
    mock_code_service,
    mock_now,
    mock_registration_policy,
) -> ReSendCodeConfirmation:
    return ReSendCodeConfirmation(
        registration_repo=mock_registration_repo,
        code_service=mock_code_service,
        event_publisher=mock_event_publisher,
        get_now=mock_now,
        policy=mock_registration_policy,
    )


@pytest.fixture
def get_registration_entity(
    creds_employee_dto,
    password_hash,
    confirmation_code,
    mock_registration_policy,
    mock_now,
) -> Callable[..., Registration]:
    return lambda: Registration.create(
        email=creds_employee_dto.email,
        password_hash=password_hash,
        confirmation_code=confirmation_code,
        confirmation_ttl=mock_registration_policy.get_confirmation_ttl(),
        now=mock_now(),
        user_agent=creds_employee_dto.user_agent,
        ip_address=creds_employee_dto.ip_address,
    )


@pytest.fixture
def password() -> Password:
    return Password("StrongPassword123!")


@pytest.fixture
def password_hash() -> PasswordHash:
    return PasswordHash(
        "$argon2id$v=19$m=65536,t=3,p=4$6S9Y9H8p7W4j5K2L1M3N4O$"
        "uV5W6X7Y8Z9A0B1C2D3E4F5G6H7I8J9K0L1M2N3O4P5"
    )


@pytest.fixture
def email(faker) -> Email:
    return Email(faker.email())
