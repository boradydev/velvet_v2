from typing import Annotated

from fastapi import Depends

from src.application.employees import cases, dtos
from src.domain.auth_sessions.vals import IpAddress, RefreshToken, UserAgent
from src.domain.employees.vals import ConfirmationCode, Email, Password
from src.presentation.fastapi.common.schemas import NullDataResponse, StandardResponse
from src.presentation.fastapi.employees import deps, schemas
from src.presentation.fastapi.employees.interfaces.cookies import IAuthCookieManager


async def register_employee(
    data: schemas.CredentialsRequest,
    case: Annotated[cases.Register, Depends(deps.get_register_case)],
    user_agent: Annotated[str, Depends(deps.get_user_agent)],
    ip_address: Annotated[str, Depends(deps.get_ip_address)],
) -> NullDataResponse:
    await case.execute(
        dto=dtos.CredentialsEmployeeDTO(
            email=Email(data.email),
            password=Password(str(data.password)),
            user_agent=UserAgent(user_agent),
            ip_address=IpAddress(ip_address),
        )
    )
    return NullDataResponse()


async def resend_confirmation_code(
    data: schemas.ResendRequest,
    case: Annotated[cases.ReSendCodeConfirmation, Depends(deps.get_resend_case)],
    ip_address: Annotated[str, Depends(deps.get_ip_address)],
) -> NullDataResponse:
    await case.execute(
        dto=dtos.ResendConfirmationCodeDTO(
            email=Email(data.email),
            ip_address=IpAddress(ip_address),
        )
    )
    return NullDataResponse()


async def confirm_employee(
    data: schemas.ConfirmRegisterRequest,
    case: Annotated[cases.ConfirmRegister, Depends(deps.get_confirm_register_case)],
    cookie: Annotated[IAuthCookieManager, Depends(deps.get_auth_cookie_manager)],
    user_agent: Annotated[str, Depends(deps.get_user_agent)],
    ip_address: Annotated[str, Depends(deps.get_ip_address)],
) -> StandardResponse[schemas.AuthTokensResponse]:
    tokens = await case.execute(
        dto=dtos.ConfirmRegisterDTO(
            email=Email(data.email),
            confirmation_code=ConfirmationCode(data.confirm_code),
            user_agent=UserAgent(user_agent),
            ip_address=IpAddress(ip_address),
        )
    )
    cookie.set_auth_cookies(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )
    return StandardResponse(
        data=schemas.AuthTokensResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
        )
    )


async def login_employee(
    data: schemas.CredentialsRequest,
    case: Annotated[cases.Login, Depends(deps.get_login_case)],
    cookies: Annotated[IAuthCookieManager, Depends(deps.get_auth_cookie_manager)],
    user_agent: Annotated[str, Depends(deps.get_user_agent)],
    ip_address: Annotated[str, Depends(deps.get_ip_address)],
) -> StandardResponse[schemas.AuthTokensResponse]:
    tokens = await case.execute(
        dto=dtos.CredentialsEmployeeDTO(
            email=Email(data.email),
            password=Password(str(data.password)),
            user_agent=UserAgent(user_agent),
            ip_address=IpAddress(ip_address),
        )
    )
    cookies.set_auth_cookies(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )
    return StandardResponse(
        data=schemas.AuthTokensResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
        )
    )


async def refresh_employee_token(
    case: Annotated[cases.Refresh, Depends(deps.get_refresh_case)],
    cookies: Annotated[IAuthCookieManager, Depends(deps.get_auth_cookie_manager)],
    user_agent: Annotated[str, Depends(deps.get_user_agent)],
    refresh_token: Annotated[str, Depends(deps.get_refresh_token)],
    ip_address: Annotated[str, Depends(deps.get_ip_address)],
) -> StandardResponse[schemas.AuthTokensResponse]:
    tokens = await case.execute(
        dto=dtos.RefreshDTO(
            refresh_token=RefreshToken(refresh_token),
            user_agent=UserAgent(user_agent),
            ip_address=IpAddress(ip_address),
        )
    )
    cookies.set_auth_cookies(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )
    return StandardResponse(
        data=schemas.AuthTokensResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
        )
    )


async def logout_employee(
    case: Annotated[cases.Logout, Depends(deps.get_logout_case)],
    cookies: Annotated[IAuthCookieManager, Depends(deps.get_auth_cookie_manager)],
    refresh_token: Annotated[str, Depends(deps.get_refresh_token)],
) -> NullDataResponse:
    await case.execute(dto=dtos.LogoutDTO(refresh_token=RefreshToken(refresh_token)))
    cookies.delete_auth_cookies()
    return NullDataResponse()
