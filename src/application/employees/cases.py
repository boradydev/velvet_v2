from collections.abc import Callable

from uuid6 import UUID

from src.application.employees import dtos, excs
from src.application.employees.services import IEmployeeTasksService
from src.core.timezone import Timedelta, Timestamp
from src.domain.auth_sessions.entity import AuthSession
from src.domain.common.interfaces import services_abc
from src.domain.employees.entities import Employee
from src.domain.employees.interfaces import uow_abc
from src.domain.employees.interfaces.repos import cache_abc
from src.domain.employees.vals import Email


class Register:
    def __init__(
        self,
        uow: uow_abc.IEmployeeUOW,
        password_service: services_abc.IPasswordService,
        get_now: Callable[[], Timestamp],
        logger: services_abc.ILogger,
    ) -> None:
        self.uow = uow
        self.password_service = password_service
        self.logger = logger
        self.get_now = get_now

    async def execute(self, dto: dtos.CredentialsEmployeeDTO) -> None:
        timestamp = self.get_now()
        password_hash = self.password_service.hashing_password(dto.password)
        async with self.uow as db:
            if await db.employees.exists_by_email(dto.email):
                raise excs.EmployeeAlreadyExistsException

            employee = Employee.register(
                email=dto.email,
                password_hash=password_hash,
                timestamp=timestamp,
            )
            await db.employees.save(employee)
            await db.commit(events=employee.pull_events())


class SendRegisterConfirmation:
    def __init__(
        self,
        code_repo: cache_abc.IConfirmationCodeRepository,
        code_ttl: int,
        email_service: services_abc.IEmailService,
        code_service: services_abc.IConfirmationCodeService,
        get_now: Callable[[], Timestamp],
        resend_cooldown: Timedelta,
    ) -> None:
        self.code_repo = code_repo
        self.code_ttl = code_ttl
        self.email_service = email_service
        self.code_service = code_service
        self.get_now = get_now
        self.resend_cooldown = resend_cooldown

    async def execute(self, dto: dtos.SendConfirmationDTO) -> None:
        timestamp = self.get_now()
        code = self.code_service.create_code()
        confirmation = dtos.ConfirmationEmployeeDTO(
            employee_id=dto.employee_id,
            email=dto.email,
            code=code,
            cooldown=timestamp + self.resend_cooldown,
        )
        await self.code_repo.save(
            email=dto.email,
            dto=confirmation,
            ttl=self.code_ttl,
        )
        await self.email_service.send(
            email=dto.email,
            message=str(code),
        )


class ReSendCodeConfirmation:
    def __init__(
        self,
        uow: uow_abc.IEmployeeUOW,
        code_repo: cache_abc.IConfirmationCodeRepository,
        task_service: IEmployeeTasksService,
        get_now: Callable[[], Timestamp],
    ) -> None:
        self.uow = uow
        self.code_repo = code_repo
        self.task_service = task_service
        self.get_now = get_now

    async def execute(self, dto: dtos.ResendCodeEmployeeDTO) -> None:
        timestamp = self.get_now()
        employee_id = await self._resolve_employee_id(
            email=dto.email,
            timestamp=timestamp,
        )
        send_confirmation = dtos.SendConfirmationDTO(
            employee_id=employee_id,
            email=dto.email,
        )
        await self.task_service.send_by_email(send_confirmation)

    async def _resolve_employee_id(
        self,
        *,
        email: Email,
        timestamp: Timestamp,
    ) -> UUID:
        confirmation = await self.code_repo.get_by_email(email)
        if confirmation:
            self._ensure_cooldown_passed(
                timestamp=timestamp,
                cooldown=confirmation.cooldown,
            )
            return confirmation.employee_id

        async with self.uow as db:
            employee_id = await db.employees.get_id_by_email(email)

        if not employee_id:
            raise excs.EmployeeNotFoundException

        return employee_id

    @staticmethod
    def _ensure_cooldown_passed(
        *,
        timestamp: Timestamp,
        cooldown: Timestamp,
    ) -> None:
        if cooldown > timestamp:
            raise excs.ConfirmationCodeActiveException


class ConfirmRegister:
    def __init__(
        self,
        uow: uow_abc.IEmployeeUOW,
        code_repo: cache_abc.IConfirmationCodeRepository,
        token_service: services_abc.ITokenService,
        get_now: Callable[[], Timestamp],
        session_expires_delta: Timedelta,
    ) -> None:
        self.uow = uow
        self.code_repo = code_repo
        self.token_service = token_service
        self.get_now = get_now
        self.session_expires_delta = session_expires_delta

    async def execute(self, dto: dtos.ConfirmRegisterDTO) -> dtos.AuthTokensDTO:
        timestamp = self.get_now()
        employee_id = await self._ensure_confirmation_code_valid(dto)
        auth_session = AuthSession.create(
            employee_id=employee_id,
            refresh_token=self.token_service.create_refresh_token(
                employee_id=employee_id,
            ),
            expires_delta=self.session_expires_delta,
            timestamp=timestamp,
        )
        async with self.uow as db:
            await db.auth_sessions.save(auth_session)

        access_token = self.token_service.create_access_token(employee_id=employee_id)
        return dtos.AuthTokensDTO(
            access_token=access_token,
            refresh_token=auth_session.refresh_token,
            device_id=auth_session.device_id,
        )

    async def _ensure_confirmation_code_valid(
        self,
        dto: dtos.ConfirmRegisterDTO,
    ) -> UUID:
        confirmation = await self.code_repo.get_by_email(dto.email)
        if not confirmation:
            raise excs.ConfirmationCodeNotFoundException

        if confirmation.code != dto.confirmation_code:
            raise excs.InvalidConfirmationCodeException

        return confirmation.employee_id


class Login:
    def __init__(
        self,
        token_service: services_abc.ITokenService,
        uow: uow_abc.IEmployeeUOW,
        password_service: services_abc.IPasswordService,
        logger: services_abc.ILogger,
        get_now: Callable[[], Timestamp],
        session_expires_delta: Timedelta,
    ):
        self.uow = uow
        self.token_service = token_service
        self.password_service = password_service
        self.logger = logger
        self.get_now = get_now
        self.session_expires_delta = session_expires_delta

    async def execute(
        self, dto: dtos.LoginCredentialsEmployeeDTO
    ) -> dtos.AuthTokensDTO:
        timestamp = self.get_now()
        async with self.uow as db:
            employee = await db.employees.get_by_email(dto.email)
            if not employee:
                raise excs.InvalidCredentialsEmployeeException

            employee.check_password(
                password=dto.password,
                password_service=self.password_service,
            )
            if dto.device_id:
                auth_session = await db.auth_sessions.get_by_device_and_employee_id(
                    employee_id=employee.id,
                    device_id=dto.device_id,
                )
                if not auth_session:
                    auth_session = self._create_auth_session(
                        employee_id=employee.id,
                        timestamp=timestamp,
                        device_id=dto.device_id,
                    )
            else:
                auth_session = self._create_auth_session(
                    employee_id=employee.id,
                    timestamp=timestamp,
                )

            self._update_refresh_token(auth_session)
            await db.auth_sessions.save(auth_session)
            await db.commit(events=auth_session.pull_events())

            return dtos.AuthTokensDTO(
                access_token=self.token_service.create_access_token(
                    employee_id=employee.id
                ),
                refresh_token=auth_session.refresh_token,
                device_id=auth_session.device_id,
            )

    def _create_auth_session(
        self,
        *,
        timestamp: Timestamp,
        employee_id: UUID,
        device_id: UUID | None = None,
    ) -> AuthSession:
        return AuthSession.create(
            employee_id=employee_id,
            expires_delta=self.session_expires_delta,
            device_id=device_id,
            timestamp=timestamp,
        )

    def _update_refresh_token(self, auth_session: AuthSession) -> None:
        auth_session.save_refresh_token(
            refresh_token=self.token_service.create_refresh_token(
                auth_session_id=auth_session.id,
            )
        )
