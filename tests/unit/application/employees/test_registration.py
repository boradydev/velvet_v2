import asyncio

import pytest

from src.application.employees.cases import Register
from src.application.employees.dtos import CredentialsEmployeeDTO
from src.application.employees.excs import EmployeeAlreadyExistsException
from src.domain.employees.entities import Employee
from src.domain.employees.vals import Email, PasswordHash


async def test_register_success(
    fake_employee_uow,
    mock_pass_service,
    mock_logger,
    mock_get_now,
):
    hashed_secret = "hashed_secret"
    mock_pass_service.hashing_password.return_value = hashed_secret

    dto = CredentialsEmployeeDTO(
        email=Email("test@test.com"),
        password="Qwerty123$",
    )
    use_case = Register(
        uow=fake_employee_uow,
        password_service=mock_pass_service,
        logger=mock_logger,
        get_now=mock_get_now,
    )

    await use_case.execute(dto)
    assert len(fake_employee_uow.employees.before_commit_employees) == 1
    assert len(fake_employee_uow.employees.after_commit_employees) == 1

    before_commit: Employee = fake_employee_uow.employees.before_commit_employees[0]
    assert before_commit.email == dto.email
    assert before_commit._password_hash == PasswordHash(hashed_secret)
    assert before_commit.is_active is True
    assert before_commit.is_verified is False
    assert len(before_commit._events) > 0

    after_commit: Employee = fake_employee_uow.employees.after_commit_employees[0]
    assert len(after_commit._events) == 0

    assert fake_employee_uow.committed is True
    assert len(fake_employee_uow.committed_events) > 0


async def test_register_unsuccess(
    mock_employee_uow,
    mock_pass_service,
    mock_logger,
    mock_get_now,
):
    dto = CredentialsEmployeeDTO(
        email=Email("test@test.com"),
        password="Qwerty123$",
    )

    mock_employee_uow.employees.exists_by_email.return_value = True
    mock_employee_uow.__aenter__.return_value = mock_employee_uow

    use_case = Register(
        uow=mock_employee_uow,
        password_service=mock_pass_service,
        logger=mock_logger,
        get_now=mock_get_now,
    )

    with pytest.raises(EmployeeAlreadyExistsException):
        await use_case.execute(dto)

    mock_employee_uow.commit.assert_not_called()
