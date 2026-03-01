from datetime import timedelta

import pytest

from src.application.employees import excs
from src.domain.employees.events import RegistrationEvent


async def test_register_success(
    creds_employee_dto,
    use_case_register,
    mock_employee_uow,
    mock_registration_repo,
    mock_event_publisher,
    mock_password_service,
    mock_code_service,
    mock_registration_policy,
    password_hash,
    confirmation_code,
) -> None:
    dto = creds_employee_dto
    mock_registration_repo.exists_by_email.return_value = False
    mock_employee_uow.__aenter__.return_value = mock_employee_uow
    mock_employee_uow.employees.exists_by_email.return_value = False
    mock_password_service.hash.return_value = password_hash
    mock_code_service.generate.return_value = confirmation_code
    mock_registration_policy.get_confirmation_ttl.return_value = timedelta(minutes=30)

    await use_case_register.execute(dto=dto)

    mock_employee_uow.__aenter__.assert_awaited_once()
    mock_employee_uow.employees.exists_by_email.assert_awaited_once_with(
        email=dto.email
    )
    mock_registration_repo.exists_by_email.assert_awaited_once_with(email=dto.email)
    mock_employee_uow.commit.assert_not_called()
    mock_employee_uow.rollback.assert_not_called()
    mock_registration_repo.save_if_not_exists.assert_awaited_once()
    mock_event_publisher.publish_many.assert_awaited_once()
    mock_code_service.generate.assert_called_once()
    mock_password_service.hash.assert_called_once_with(password=dto.password)
    mock_registration_policy.get_confirmation_ttl.assert_called_once()

    event_kwargs = mock_event_publisher.publish_many.call_args.kwargs
    published_events: list[RegistrationEvent] = event_kwargs["events"]
    assert published_events[0].email == dto.email
    assert published_events[0].confirmation_code == confirmation_code


async def test_register_fails_if_registration_exists_in_cache(
    creds_employee_dto,
    use_case_register,
    mock_registration_repo,
    mock_code_service,
    mock_event_publisher,
) -> None:
    dto = creds_employee_dto
    mock_registration_repo.exists_by_email.return_value = True

    with pytest.raises(excs.RegistrationAlreadyExistsException):
        await use_case_register.execute(dto=dto)

    mock_registration_repo.exists_by_email.assert_awaited_once_with(email=dto.email)
    mock_code_service.generate.assert_not_called()
    mock_registration_repo.save_if_not_exists.assert_not_called()
    mock_event_publisher.publish_many.assert_not_called()


async def test_register_fails_if_employee_exists_in_db(
    creds_employee_dto,
    use_case_register,
    mock_employee_uow,
    mock_registration_repo,
    mock_code_service,
    mock_event_publisher,
) -> None:
    dto = creds_employee_dto
    mock_registration_repo.exists_by_email.return_value = False
    mock_employee_uow.__aenter__.return_value = mock_employee_uow
    mock_employee_uow.employees.exists_by_email.return_value = True

    with pytest.raises(excs.EmployeeAlreadyExistsException):
        await use_case_register.execute(dto=dto)

    mock_employee_uow.employees.exists_by_email.assert_awaited_once_with(
        email=dto.email
    )
    mock_code_service.generate.assert_not_called()
    mock_registration_repo.save_if_not_exists.assert_not_called()
    mock_event_publisher.publish_many.assert_not_called()
