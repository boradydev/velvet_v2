from typing import Annotated

from fastapi import Depends

from src.application.employees import cases, dtos
from src.presentation.fastapi.common.schemas import NullDataResponse
from src.presentation.fastapi.employees import deps, schemas
from src.presentation.fastapi.employees.interfaces.cookie import IAuthCookieManager


async def register_employee(
    data: schemas.RegisterRequest,
    case: Annotated[cases.Register, Depends(deps.get_register_case)],
) -> NullDataResponse:
    await case.execute(
        dtos.CredentialsEmployeeDTO(
            email=data.email,
            password=str(data.password),
        )
    )
    return NullDataResponse()


async def resend_confirmation_code(
    data: schemas.ResendRequest,
    case: Annotated[cases.ReSendCodeConfirmation, Depends(deps.get_resend_case)],
) -> NullDataResponse:
    await case.execute(
        dtos.ResendCodeEmployeeDTO(
            email=data.email,
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
            email=data.email,
            confirmation_code=data.confirm_code,
        )
    )
    cookie.set_auth_cookies(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        device_id=tokens.device_id,
    )
    return schemas.AuthTokensResponse(
        access_token=tokens.access_token,
        refresh_token=tokens.refresh_token,
        device_id=tokens.device_id,
    )
