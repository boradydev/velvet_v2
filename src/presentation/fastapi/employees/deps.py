from typing import Annotated

from fastapi import Depends, Request, Response

from src.application.employees import cases
from src.infrastructure.common.resources import AppState, LifespanState
from src.infrastructure.web.fastapi.cookies import AuthCookieManager
from src.presentation.fastapi.common.common_deps import get_lifespan_state
from src.presentation.fastapi.employees.interfaces.cookie import IAuthCookieManager


def get_register_case(
    lifespan: Annotated[LifespanState, Depends(get_lifespan_state)],
) -> cases.Register:
    return lifespan.cases.employees.create_register_case()


def get_confirm_register_case(
    lifespan: Annotated[LifespanState, Depends(get_lifespan_state)],
) -> cases.ConfirmRegister:
    return lifespan.cases.employees.create_confirm_register_case()


def get_resend_case(
    lifespan: Annotated[LifespanState, Depends(get_lifespan_state)],
) -> cases.ReSendCodeConfirmation:
    return lifespan.cases.employees.create_resend_case()


def get_auth_cookie_manager(
    app_state: Annotated[AppState, Depends(get_lifespan_state)],
    request: Request,
    response: Response,
) -> IAuthCookieManager:
    return AuthCookieManager(
        request=request,
        response=response,
        settings=app_state.settings.jwt,
    )


def get_user_agent(
    cookies: Annotated[IAuthCookieManager, Depends(get_auth_cookie_manager)],
) -> str:
    return cookies.user_agent
