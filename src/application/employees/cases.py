from collections.abc import Callable

from uuid6 import UUID

from src.application.common.interfaces import IEventPublisher
from src.application.employees import dtos, excs
from src.core.timezone import Timestamp
from src.domain.auth_sessions.entity import AuthSession
from src.domain.common.interfaces import services_abc
from src.domain.employees.entities import Employee, Registration
from src.domain.employees.interfaces import uow_abc
from src.domain.employees.interfaces.policies import (
    IAuthorizationPolicy,
    IRegistrationPolicy,
)
from src.domain.employees.interfaces.repos.cache_abc import IRegistrationRepository


class Register:
    def __init__(
        self,
        *,
        uow: uow_abc.IEmployeeUOW,
        registration_repo: IRegistrationRepository,
        event_publisher: IEventPublisher,
        password_service: services_abc.IPasswordService,
        code_service: services_abc.IConfirmationCodeService,
        get_now: Callable[[], Timestamp],
        policy: IRegistrationPolicy,
    ) -> None:
        self.uow = uow
        self.registration_repo = registration_repo
        self.event_publisher = event_publisher
        self.password_service = password_service
        self.code_service = code_service
        self.get_now = get_now
        self.policy = policy

    async def execute(self, *, dto: dtos.CredentialsEmployeeDTO) -> None:
        now = self.get_now()
        if await self.registration_repo.exists_by_email(email=dto.email):
            raise excs.RegistrationAlreadyExistsException

        async with self.uow as uow:
            if await uow.employees.exists_by_email(email=dto.email):
                raise excs.EmployeeAlreadyExistsException

        registration = Registration.create(
            email=dto.email,
            password_hash=self.password_service.hash(password=dto.password),
            user_agent=dto.user_agent,
            ip_address=dto.ip_address,
            now=now,
            confirmation_code=self.code_service.generate(),
            confirmation_ttl=self.policy.get_confirmation_ttl(),
        )
        await self.registration_repo.save_if_not_exists(
            email=dto.email,
            dto=registration,
            ttl=registration.time_left(now=now),
        )
        await self.event_publisher.publish_many(events=registration.pull_events())


class SendConfirmation:
    def __init__(
        self,
        *,
        email_service: services_abc.IEmailService,
    ) -> None:
        self.email_service = email_service

    async def execute(self, *, dto: dtos.SendConfirmationCodeDTO) -> None:
        await self.email_service.send_confirmation_code(dto=dto)


class ReSendCodeConfirmation:
    def __init__(
        self,
        *,
        registration_repo: IRegistrationRepository,
        event_publisher: IEventPublisher,
        code_service: services_abc.IConfirmationCodeService,
        get_now: Callable[[], Timestamp],
        policy: IRegistrationPolicy,
    ) -> None:
        self.registration_repo = registration_repo
        self.event_publisher = event_publisher
        self.code_service = code_service
        self.get_now = get_now
        self.policy = policy

    async def execute(self, *, dto: dtos.ResendConfirmationCodeDTO) -> None:
        now = self.get_now()
        registration = await self.registration_repo.find_by_email(email=dto.email)
        if not registration:
            raise excs.RegistrationNotFound

        min_ttl = self.policy.get_min_resend_ttl()
        if not registration.has_enough_time_left(now=now, min_ttl=min_ttl):
            raise excs.TooLateToResend

        cooldown = self.policy.get_cooldown(resend_count=registration.resend_count)
        if not registration.can_resend(now=now, cooldown=cooldown):
            raise excs.CooldownNotExpired

        new_code = self.code_service.generate()
        registration.resend(
            new_code=new_code,
            now=now,
        )
        await self.registration_repo.save_if_version_matches(
            email=registration.email,
            dto=registration,
            ttl=registration.time_left(now=now),
        )
        await self.event_publisher.publish_many(events=registration.pull_events())


class ConfirmRegister:
    def __init__(
        self,
        *,
        uow: uow_abc.IEmployeeUOW,
        registration_repo: IRegistrationRepository,
        token_service: services_abc.ITokenService,
        get_now: Callable[[], Timestamp],
        id_generator: Callable[[], UUID],
        reg_policy: IRegistrationPolicy,
        auth_policy: IAuthorizationPolicy,
    ) -> None:
        self.uow = uow
        self.registration_repo = registration_repo
        self.token_service = token_service
        self.get_now = get_now
        self.id_generator = id_generator
        self.reg_policy = reg_policy
        self.auth_policy = auth_policy

    async def execute(self, *, dto: dtos.ConfirmRegisterDTO) -> dtos.AuthTokensDTO:
        now = self.get_now()
        registration = await self.registration_repo.find_by_email(email=dto.email)
        if not registration:
            raise excs.RegistrationNotFound

        registration.confirm(
            code=dto.confirmation_code,
            now=now,
        )
        async with self.uow as uow:
            role = await uow.roles.get_by_name(
                role_name=self.auth_policy.get_default_role()
            )
            employee_id = self.id_generator()
            employee = Employee.create(
                employee_id=employee_id,
                email=registration.email,
                password_hash=registration.password_hash,
                role_id=role.id,
                now=now,
            )
            session_id = self.id_generator()
            session_expires_at = self.reg_policy.get_refresh_session_expires_at(now=now)
            refresh_token = self.token_service.create_refresh_token(
                employee_id=employee_id,
                session_id=session_id,
                expires_at=session_expires_at,
            )
            refresh_token_hash = self.token_service.hash_refresh_token(
                refresh_token=refresh_token
            )
            auth_session = AuthSession.create(
                session_id=session_id,
                employee_id=employee_id,
                user_agent=registration.user_agent,
                ip_address=registration.ip_address,
                refresh_token_hash=refresh_token_hash,
                expires_at=session_expires_at,
                now=now,
            )
            await uow.employees.add(employee=employee)
            await uow.auth_sessions.save(auth_session=auth_session)
            await self.registration_repo.delete_by_email(email=registration.email)
            await uow.commit(
                events=registration.pull_events()
                + employee.pull_events()
                + auth_session.pull_events()
            )

        access_token = self.token_service.create_access_token(
            employee_id=employee_id,
            expires_at=self.reg_policy.get_access_expires_at(now=now),
        )
        return dtos.AuthTokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )


class Login:
    def __init__(
        self,
        *,
        token_service: services_abc.ITokenService,
        uow: uow_abc.IEmployeeUOW,
        password_service: services_abc.IPasswordService,
        get_now: Callable[[], Timestamp],
        id_generator: Callable[[], UUID],
        policy: IRegistrationPolicy,
    ):
        self.uow = uow
        self.token_service = token_service
        self.password_service = password_service
        self.get_now = get_now
        self.id_generator = id_generator
        self.policy = policy

    async def execute(
        self,
        *,
        dto: dtos.CredentialsEmployeeDTO,
    ) -> dtos.AuthTokensDTO:
        now = self.get_now()
        async with self.uow as uow:
            employee = await uow.employees.find_by_email(email=dto.email)
            if not employee or not self.password_service.verify_password(
                plain_password=dto.password,
                hashed_password=employee.password_hash,
            ):
                raise excs.InvalidCredentialsEmployeeException

            session_id = self.id_generator()
            session_expires_at = self.policy.get_refresh_session_expires_at(now=now)
            refresh_token = self.token_service.create_refresh_token(
                employee_id=employee.id,
                session_id=session_id,
                expires_at=session_expires_at,
            )
            refresh_token_hash = self.token_service.hash_refresh_token(
                refresh_token=refresh_token,
            )
            auth_session = AuthSession.create(
                session_id=session_id,
                employee_id=employee.id,
                user_agent=dto.user_agent,
                ip_address=dto.ip_address,
                refresh_token_hash=refresh_token_hash,
                expires_at=session_expires_at,
                now=now,
            )

            await uow.auth_sessions.save(auth_session=auth_session)
            await uow.commit(events=auth_session.pull_events())

            access_token = self.token_service.create_access_token(
                employee_id=employee.id,
                expires_at=self.policy.get_access_expires_at(now=now),
            )
            return dtos.AuthTokensDTO(
                access_token=access_token,
                refresh_token=refresh_token,
            )


class Refresh:
    def __init__(
        self,
        *,
        uow: uow_abc.IEmployeeUOW,
        token_service: services_abc.ITokenService,
        policy: IRegistrationPolicy,
        get_now: Callable[[], Timestamp],
    ) -> None:
        self.uow = uow
        self.token_service = token_service
        self.policy = policy
        self.get_now = get_now

    async def execute(
        self,
        *,
        dto: dtos.RefreshDTO,
    ) -> dtos.AuthTokensDTO:
        now = self.get_now()
        payload = self.token_service.get_payload_refresh_token(
            refresh_token=dto.refresh_token.value
        )
        async with self.uow as uow:
            auth_session = await uow.auth_sessions.get(
                auth_session_id=payload.auth_session_id,
                employee_id=payload.employee_id,
            )
            if not self.token_service.verify_hash_refresh_token(
                plain_token=dto.refresh_token.value,
                hashed_token=auth_session.refresh_token_hash,
            ):
                auth_session.flag_theft_attempt(
                    now=now,
                    requested_by=payload.employee_id,
                )
                await uow.auth_sessions.delete(auth_session=auth_session)
                await uow.commit(events=auth_session.pull_events())
                raise excs.InvalidRefreshTokenException

            session_expires_at = self.policy.get_refresh_session_expires_at(now=now)
            refresh_token = self.token_service.create_refresh_token(
                employee_id=auth_session.employee_id,
                session_id=auth_session.id,
                expires_at=session_expires_at,
            )
            new_hash = self.token_service.hash_refresh_token(
                refresh_token=refresh_token
            )
            auth_session.rotate(
                requested_by=payload.employee_id,
                new_hash=new_hash,
                expires_at=session_expires_at,
                now=now,
            )
            await uow.auth_sessions.save(auth_session=auth_session)
            await uow.commit(events=auth_session.pull_events())

        access_token = self.token_service.create_access_token(
            employee_id=auth_session.employee_id,
            expires_at=self.policy.get_access_expires_at(now=now),
        )
        return dtos.AuthTokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )


class Logout:
    def __init__(
        self,
        *,
        uow: uow_abc.IEmployeeUOW,
        token_service: services_abc.ITokenService,
        get_now: Callable[[], Timestamp],
    ) -> None:
        self.uow = uow
        self.token_service = token_service
        self.get_now = get_now

    async def execute(
        self,
        *,
        dto: dtos.LogoutDTO,
    ) -> None:
        now = self.get_now()
        payload = self.token_service.get_payload_refresh_token(
            refresh_token=dto.refresh_token.value
        )
        async with self.uow as uow:
            auth_session = await uow.auth_sessions.get(
                auth_session_id=payload.auth_session_id,
                employee_id=payload.employee_id,
            )
            auth_session.close(
                now=now,
                requested_by=payload.employee_id,
            )
            await uow.auth_sessions.delete(auth_session=auth_session)
            await uow.commit(events=auth_session.pull_events())
