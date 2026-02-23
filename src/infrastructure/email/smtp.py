from src.domain.common.interfaces.services_abc import IEmailService
from src.domain.employees.vals import Email


class EmailService(IEmailService):  # todo затычка для отправки проверочного кода
    def send(self, email: Email, message: str):
        print(f"{email.value}: {message}")
