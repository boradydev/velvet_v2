from unittest.mock import AsyncMock, MagicMock

import pytest

from src.application.employees.dtos import CredentialsEmployeeDTO
from src.application.employees.excs import EmployeeAlreadyExistsException
from src.application.employees.cases import Register
from src.domain.employees.vals import Email


@pytest.mark.parametrize(
    "test_password",
    [
        "Qwer123$",
        "Qwer123$124",
    ],
)
async def test_register_success(test_password):
    uow = AsyncMock()
    pass_service = MagicMock()
    code_service = MagicMock()
    mail_service = MagicMock()
    logger = MagicMock()

    dto = CredentialsEmployeeDTO(email="test@test.com", password=test_password)
    confirm_code = "123456"

    uow.employees.exists_by_email.return_value = False
    uow.__aenter__.return_value = uow

    pass_service.hashing_password.return_value = "hashed_secret"
    code_service.create_code.return_value = confirm_code

    interactor = Register(
        uow=uow,
        password_service=pass_service,
        confirmation_code_service=code_service,
        send_email_service=mail_service,
        logger=logger,
    )

    await interactor.execute(dto)

    pass_service.hashing_password.assert_called_once_with(dto.password)

    mail_service.send.assert_called_once_with(
        email=Email(value=dto.email), message=confirm_code
    )

    uow.commit.assert_called_once()


async def test_register_unsuccess():
    uow = AsyncMock()
    pass_service = MagicMock()
    code_service = MagicMock()
    mail_service = MagicMock()
    logger = MagicMock()

    dto = CredentialsEmployeeDTO(email="test@test.com", password="Qwer123$")
    confirm_code = "123456"

    uow.employees.exists_by_email.return_value = True
    uow.__aenter__.return_value = uow

    pass_service.hashing_password.return_value = "hashed_secret"
    code_service.create_code.return_value = confirm_code

    interactor = Register(
        uow=uow,
        password_service=pass_service,
        confirmation_code_service=code_service,
        send_email_service=mail_service,
        logger=logger,
    )

    with pytest.raises(EmployeeAlreadyExistsException):
        await interactor.execute(dto)

    uow.commit.assert_not_called()
    mail_service.send.assert_not_called()
