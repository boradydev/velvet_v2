from datetime import timedelta

from uuid6 import uuid7

from src.application.employees.cases import SendRegisterConfirmation
from src.application.employees.dtos import SendConfirmationDTO
from src.domain.employees.vals import ConfirmationCode, Email


async def test_send_confirmation_success(
    fake_confirmation_code_repo,
    mock_email_service,
    mock_code_service,
        mock_get_now,
) -> None:
    test_code = ConfirmationCode("123456")
    test_ttl = 300
    test_cooldown = timedelta(minutes=1)
    mock_code_service.create_code.return_value = test_code

    use_case = SendRegisterConfirmation(
        code_repo=fake_confirmation_code_repo,
        code_ttl=test_ttl,
        email_service=mock_email_service,
        code_service=mock_code_service,
        resend_cooldown=test_cooldown,
        get_now=mock_get_now,
    )

    dto = SendConfirmationDTO(
        employee_id=uuid7(),
        email=Email("employee@shop.com"),
    )

    await use_case.execute(dto)

    assert dto.email in fake_confirmation_code_repo.storage
    saved_data = fake_confirmation_code_repo.storage[dto.email]

    assert saved_data.ttl == test_ttl

    saved_dto = saved_data.dto
    assert saved_dto.employee_id == dto.employee_id
    assert saved_dto.code == test_code

    assert saved_dto.cooldown > mock_get_now()
    assert saved_dto.cooldown == mock_get_now() + test_cooldown

    mock_email_service.send.assert_awaited_once_with(
        email=dto.email, message=str(test_code)
    )
    mock_code_service.create_code.assert_called_once()
