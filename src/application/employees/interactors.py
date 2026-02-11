from src.application.employees import exceptions
from src.application.employees.dto import CredentialsEmployeeDTO
from src.application.services.code import IConfirmationCodeService
from src.application.services.send import IEmailService
from src.application.services.token import ITokenService
from src.domain.employees.entities import Employee
from src.domain.employees.interfaces import (
    IEmployeeUOW,
    IPasswordService,
)


class RegisterInteractor:
    uow: IEmployeeUOW
    password_service: IPasswordService
    confirmation_code_service: IConfirmationCodeService
    send_email_service: IEmailService

    def __init__(
        self,
        uow: IEmployeeUOW,
        password_service: IPasswordService,
        confirmation_code_service: IConfirmationCodeService,
        send_email_service: IEmailService,
    ):
        self.uow = uow
        self.password_service = password_service
        self.confirmation_code_service = confirmation_code_service
        self.send_email_service = send_email_service

    async def register(self, dto: CredentialsEmployeeDTO) -> None:
        password_hash = self.password_service.hashing_password(dto.password)
        async with self.uow as db:
            if await db.employees.exists_by_email(dto.email):
                raise exceptions.EmployeeAlreadyExistsException

            employee = Employee.register(
                email=dto.email,
                password_hash=password_hash,
            )
            await db.employees.add(employee)
            await db.commit()

        self.send_email_service.send(
            email=employee.email,
            message=self.confirmation_code_service.create_code(),
        )


class LoginInteractor:
    uow: IEmployeeUOW
    token_service: ITokenService
    password_service: IPasswordService

    def __init__(
        self,
        token_service: ITokenService,
        uow: IEmployeeUOW,
        password_service: IPasswordService,
    ):
        self.uow = uow
        self.token_service = token_service
        self.password_service = password_service

    async def register(self, dto: CredentialsEmployeeDTO) -> None:
        pass
