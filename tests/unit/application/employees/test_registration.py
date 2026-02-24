from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.employees.cases import Register
from src.application.employees.dtos import CredentialsEmployeeDTO
from src.application.employees.excs import EmployeeAlreadyExistsException
from src.domain.employees.entities import Employee
from src.domain.employees.vals import Email, PasswordHash


async def test_register_success(employee_uow):
    uow = employee_uow
    pass_service = MagicMock()
    hashed_secret = "hashed_secret"
    pass_service.hashing_password.return_value = hashed_secret

    dto = CredentialsEmployeeDTO(email=Email("test@test.com"), password="Qwerty123$")
    use_case = Register(
        uow=uow,
        password_service=pass_service,
        logger=MagicMock(),
    )

    await use_case.execute(dto)
    assert len(uow.employees.before_commit_employees) == 1
    assert len(uow.employees.after_commit_employees) == 1

    before_commit: Employee = uow.employees.before_commit_employees[0]
    assert before_commit.email == dto.email
    assert before_commit._password_hash == PasswordHash(hashed_secret)
    assert before_commit.is_active is True
    assert before_commit.is_verified is False
    assert len(before_commit._events) > 0

    after_commit: Employee = uow.employees.after_commit_employees[0]
    assert len(after_commit._events) == 0

    assert uow.committed is True
    assert len(uow.committed_events) > 0


async def test_register_unsuccess():
    uow = AsyncMock()
    pass_service = MagicMock()
    logger = MagicMock()

    dto = CredentialsEmployeeDTO(email=Email("test@test.com"), password="Qwerty123$")

    uow.employees.exists_by_email.return_value = True
    uow.__aenter__.return_value = uow

    use_case = Register(
        uow=uow,
        password_service=pass_service,
        logger=logger,
    )

    with pytest.raises(EmployeeAlreadyExistsException):
        await use_case.execute(dto)

    uow.commit.assert_not_called()
