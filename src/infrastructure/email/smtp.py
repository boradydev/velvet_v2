from src.application.employees.dtos import SendConfirmationCodeDTO


class EmailService:
    async def send_confirmation_code(self, *, dto: SendConfirmationCodeDTO) -> None:
        raise NotImplementedError
