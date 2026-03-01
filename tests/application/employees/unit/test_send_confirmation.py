from datetime import timedelta

from uuid6 import uuid7

from src.application.employees.cases import SendConfirmation
from src.application.employees.dtos import SendConfirmationCodeDTO
from src.domain.employees.vals import ConfirmationCode, Email


async def test_send_confirmation_success(
    mock_email_service,
    faker,
) -> None:
    dto = SendConfirmationCodeDTO(
        email=Email(faker.email()),
        confirmation_code=ConfirmationCode(faker.bothify(text="######")),
    )
    use_case = SendConfirmation(email_service=mock_email_service)
    await use_case.execute(dto=dto)
    mock_email_service.send_confirmation_code.assert_awaited_once_with(dto=dto)