from src.application.employees import exceptions
from src.application.employees.dto import CredentialsEmployeeDTO
from src.application.services.code import IConfirmationCodeService
from src.application.services.logger import ILogger
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
    logger: ILogger

    def __init__(
        self,
        uow: IEmployeeUOW,
        password_service: IPasswordService,
        logger: ILogger,
    ):
        self.uow = uow
        self.password_service = password_service
        self.logger = logger

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
            await db.commit(events=employee.pull_events())


class LoginInteractor:
    uow: IEmployeeUOW
    token_service: ITokenService
    password_service: IPasswordService
    logger: ILogger

    def __init__(
        self,
        token_service: ITokenService,
        uow: IEmployeeUOW,
        password_service: IPasswordService,
        logger: ILogger,
    ):
        self.uow = uow
        self.token_service = token_service
        self.password_service = password_service
        self.logger = logger

    async def login(self, dto: CredentialsEmployeeDTO) -> None:
        pass
