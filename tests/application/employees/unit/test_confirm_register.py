from datetime import timedelta

import pytest
from uuid6 import uuid7

from src.application.employees import dtos, excs
from src.application.employees.cases import ConfirmRegister
from src.domain.employees.vals import ConfirmationCode, Email


async def test_confirm_register_success(
    mock_registration_repo,
    mock_employee_uow,
    mock_token_service,
    mock_now,
    faker,
) -> None:
    # Arrange
    test_email = Email(faker.email())
    test_employee_id = uuid7()
    test_code = ConfirmationCode(faker.bothify(text="######"))
    test_expires_delta = timedelta(days=1)

    test_access_token = "access_token_abc"
    test_refresh_token = "refresh_token_xyz"

    cache_dto = dtos.ConfirmationEmployeeDTO(
        employee_id=test_employee_id,
        email=test_email,
        code=test_code,
        cooldown=mock_now() - timedelta(seconds=1),
    )
    mock_registration_repo.get_by_email.return_value = cache_dto

    # Настраиваем сервис токенов
    mock_token_service.create_access_token.return_value = test_access_token
    mock_token_service.create_refresh_token.return_value = test_refresh_token

    mock_employee_uow.__aenter__.return_value = mock_employee_uow

    use_case = ConfirmRegister(
        uow=mock_employee_uow,
        code_repo=mock_registration_repo,
        token_service=mock_token_service,
        get_now=mock_now,
        session_expires_delta=test_expires_delta,
    )

    dto = dtos.ConfirmRegisterDTO(
        email=test_email,
        confirmation_code=test_code,
    )

    # Act
    result = await use_case.execute(dto)

    # Assert
    assert isinstance(result, dtos.AuthTokensDTO)
    assert result.access_token == test_access_token
    assert result.refresh_token == test_refresh_token

    # Проверяем сохранение сессии
    mock_employee_uow.auth_sessions.save.assert_awaited_once()
    mock_employee_uow.commit.assert_awaited_once()
    mock_employee_uow.rollback.assert_not_called()
    mock_registration_repo.delete_by_email.assert_awaited_once_with(
        email=test_email
    )
    mock_token_service.create_refresh_token.assert_awaited_once_with(
        employee_id=test_employee_id
    )
    mock_token_service.create_access_token.assert_awaited_once_with(
        employee_id=test_employee_id
    )
    saved_session = mock_employee_uow.auth_sessions.save.call_args[0][0]
    assert saved_session.employee_id == test_employee_id
    assert saved_session.refresh_token == test_refresh_token


async def test_confirm_register_invalid_code(
    mock_registration_repo,
    mock_employee_uow,
    mock_token_service,
    mock_now,
    faker,
) -> None:
    # Arrange
    test_email = Email(faker.email())
    correct_code = ConfirmationCode("111111")
    wrong_code = ConfirmationCode("222222")

    cache_dto = dtos.ConfirmationEmployeeDTO(
        employee_id=uuid7(),
        email=test_email,
        code=correct_code,
        cooldown=mock_now(),
    )
    mock_registration_repo.get_by_email.return_value = cache_dto

    use_case = ConfirmRegister(
        uow=mock_employee_uow,
        code_repo=mock_registration_repo,
        token_service=mock_token_service,
        get_now=mock_now,
        session_expires_delta=timedelta(hours=1),
    )

    dto = dtos.ConfirmRegisterDTO(email=test_email, confirmation_code=wrong_code)

    # Act & Assert
    with pytest.raises(excs.InvalidConfirmationCodeException):
        await use_case.execute(dto)

    mock_employee_uow.__aenter__.assert_not_called()
    mock_token_service.create_access_token.assert_not_called()


async def test_confirm_register_code_not_found(
    mock_registration_repo,
    mock_employee_uow,
    mock_token_service,
    mock_now,
    faker,
) -> None:
    # Arrange
    mock_registration_repo.get_by_email.return_value = None

    use_case = ConfirmRegister(
        uow=mock_employee_uow,
        code_repo=mock_registration_repo,
        token_service=mock_token_service,
        get_now=mock_now,
        session_expires_delta=timedelta(hours=1),
    )

    dto = dtos.ConfirmRegisterDTO(
        email=Email(faker.email()),
        confirmation_code=ConfirmationCode("123456"),
    )

    # Act & Assert
    with pytest.raises(excs.ConfirmationCodeNotFoundException):
        await use_case.execute(dto)

    mock_token_service.create_refresh_token.assert_not_called()
    mock_employee_uow.auth_sessions.save.assert_not_called()
