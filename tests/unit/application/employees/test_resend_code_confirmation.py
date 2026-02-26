from datetime import timedelta

import pytest
from uuid6 import uuid7

from src.application.employees import dtos, excs
from src.application.employees.cases import ReSendCodeConfirmation
from src.domain.employees.vals import ConfirmationCode, Email


async def test_resend_confirmation_from_cache_success(
    mock_confirmation_code_repo,
    mock_employee_uow,
    mock_task_service,
    mock_get_now,
    faker,
) -> None:
    test_email = Email(faker.email())
    test_employee_id = uuid7()

    past_cooldown = mock_get_now() - timedelta(seconds=1)
    dto = dtos.ConfirmationEmployeeDTO(
        employee_id=test_employee_id,
        email=test_email,
        code=ConfirmationCode(faker.bothify(text="######")),
        cooldown=past_cooldown,
    )
    mock_confirmation_code_repo.get_by_email.return_value = dto

    use_case = ReSendCodeConfirmation(
        uow=mock_employee_uow,
        code_repo=mock_confirmation_code_repo,
        task_service=mock_task_service,
        get_now=mock_get_now,
    )
    dto = dtos.ResendCodeEmployeeDTO(email=test_email)
    await use_case.execute(dto)

    expected_send_dto = dtos.SendConfirmationDTO(
        employee_id=test_employee_id,
        email=test_email,
    )
    mock_task_service.send_by_email.assert_awaited_once_with(expected_send_dto)
    mock_employee_uow.employees.get_id_by_email.assert_not_called()
    mock_employee_uow.__aenter__.assert_not_called()
    mock_employee_uow.commit.assert_not_called()
    mock_employee_uow.rollback.assert_not_called()


async def test_resend_confirmation_from_db_success(
    mock_confirmation_code_repo,
    mock_employee_uow,
    mock_task_service,
    mock_get_now,
    faker,
) -> None:
    test_email = Email(faker.email())
    test_employee_id = uuid7()

    mock_confirmation_code_repo.get_by_email.return_value = None
    mock_employee_uow.__aenter__.return_value = mock_employee_uow
    mock_employee_uow.employees.get_id_by_email.return_value = test_employee_id

    use_case = ReSendCodeConfirmation(
        uow=mock_employee_uow,
        code_repo=mock_confirmation_code_repo,
        task_service=mock_task_service,
        get_now=mock_get_now,
    )
    dto = dtos.ResendCodeEmployeeDTO(email=test_email)
    await use_case.execute(dto)

    mock_confirmation_code_repo.get_by_email.assert_awaited_once_with(test_email)
    mock_employee_uow.employees.get_id_by_email.assert_awaited_once_with(test_email)
    mock_employee_uow.__aenter__.assert_awaited_once()
    mock_employee_uow.commit.assert_not_called()
    mock_employee_uow.rollback.assert_not_called()

    expected_send_dto = dtos.SendConfirmationDTO(
        employee_id=test_employee_id,
        email=test_email,
    )
    mock_task_service.send_by_email.assert_awaited_once_with(expected_send_dto)


async def test_resend_confirmation_from_db_not_found(
    mock_confirmation_code_repo,
    mock_employee_uow,
    mock_task_service,
    mock_get_now,
    faker,
) -> None:
    test_email = Email(faker.email())
    mock_confirmation_code_repo.get_by_email.return_value = None
    mock_employee_uow.__aenter__.return_value = mock_employee_uow
    mock_employee_uow.employees.get_id_by_email.return_value = None

    use_case = ReSendCodeConfirmation(
        uow=mock_employee_uow,
        code_repo=mock_confirmation_code_repo,
        get_now=mock_get_now,
        task_service=mock_task_service,
    )
    dto = dtos.ResendCodeEmployeeDTO(email=test_email)
    with pytest.raises(excs.EmployeeNotFoundException):
        await use_case.execute(dto)

    mock_employee_uow.__aenter__.assert_awaited_once()
    mock_confirmation_code_repo.get_by_email.assert_awaited_once_with(test_email)
    mock_employee_uow.employees.get_id_by_email.assert_awaited_once_with(test_email)
    mock_task_service.send_by_email.assert_not_called()
    mock_employee_uow.commit.assert_not_called()
    mock_employee_uow.rollback.assert_not_called()


async def test_resend_confirmation_from_cache_cooldown_active(
    mock_confirmation_code_repo,
    mock_employee_uow,
    mock_task_service,
    mock_get_now,
    faker,
) -> None:
    test_email = Email(faker.email())
    test_employee_id = uuid7()

    active_cooldown = mock_get_now() + timedelta(seconds=1)
    cache_dto = dtos.ConfirmationEmployeeDTO(
        employee_id=test_employee_id,
        email=test_email,
        code=ConfirmationCode(faker.bothify(text="######")),
        cooldown=active_cooldown,
    )
    mock_confirmation_code_repo.get_by_email.return_value = cache_dto

    dto = dtos.ResendCodeEmployeeDTO(email=test_email)
    use_case = ReSendCodeConfirmation(
        uow=mock_employee_uow,
        code_repo=mock_confirmation_code_repo,
        task_service=mock_task_service,
        get_now=mock_get_now,
    )
    with pytest.raises(excs.ConfirmationCodeActiveException):
        await use_case.execute(dto)

    mock_employee_uow.__aenter__.assert_not_called()
    mock_employee_uow.employees.get_id_by_email.assert_not_called()
    mock_task_service.send_by_email.assert_not_called()
    mock_employee_uow.commit.assert_not_called()
    mock_employee_uow.rollback.assert_not_called()
