from src.application.services.send import IEmailService
from src.domain.employees.value_objects import Email


class EmailService(IEmailService):  # todo затычка для отправки проверочного кода
    def send(self, email: Email, message: str):
        print(f"{email.value}: {message}")
