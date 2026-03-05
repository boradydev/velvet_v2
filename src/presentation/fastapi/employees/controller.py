from typing import Annotated

from fastapi import Depends

from src.application.employees import cases, dtos
from src.domain.auth_sessions.vals import UserAgent
from src.domain.employees.vals import ConfirmationCode, Email, Password
from src.presentation.fastapi.common.schemas import NullDataResponse
from src.presentation.fastapi.employees import deps, schemas
from src.presentation.fastapi.employees.interfaces.cookie import IAuthCookieManager


async def register_employee(
    data: schemas.RegisterRequest,
    case: Annotated[cases.Register, Depends(deps.get_register_case)],
    user_agent: Annotated[str, Depends(deps.get_user_agent)],
) -> NullDataResponse:
    await case.execute(
        dto=dtos.CredentialsEmployeeDTO(
            email=Email(data.email),
            password=Password(str(data.password)),
            user_agent=UserAgent(user_agent),
        )
    )
    return NullDataResponse()


async def resend_confirmation_code(
    data: schemas.ResendRequest,
    case: Annotated[cases.ReSendCodeConfirmation, Depends(deps.get_resend_case)],
) -> NullDataResponse:
    await case.execute(
        dto=dtos.ResendConfirmationCodeDTO(
            email=Email(data.email),
        )
    )
    return NullDataResponse()


async def confirm_employee(
    data: schemas.ConfirmRegisterRequest,
    case: Annotated[cases.ConfirmRegister, Depends(deps.get_confirm_register_case)],
    cookie: Annotated[IAuthCookieManager, Depends(deps.get_auth_cookie_manager)],
) -> schemas.AuthTokensResponse:
    tokens = await case.execute(
        dto=dtos.ConfirmRegisterDTO(
            email=Email(data.email),
            confirmation_code=ConfirmationCode(data.confirm_code),
        )
    )
    cookie.set_auth_cookies(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )
    return schemas.AuthTokensResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
    )
