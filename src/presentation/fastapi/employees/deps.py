from typing import Annotated

from fastapi import Depends, Request, Response

from src.application.employees import cases
from src.infrastructure.common.resources import AppState, LifespanState
from src.infrastructure.web.fastapi.cookies import AuthCookieManager
from src.presentation.fastapi.common.common_deps import get_lifespan_state
from src.presentation.fastapi.employees.interfaces.cookies import IAuthCookieManager
from src.presentation.fastapi.employees.interfaces.headers import ISystemHeaderManager


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



def get_login_case(
    lifespan: Annotated[LifespanState, Depends(get_lifespan_state)],
) -> cases.Login:
    return lifespan.cases.employees.create_login_case()


def get_logout_case(
    lifespan: Annotated[LifespanState, Depends(get_lifespan_state)],
) -> cases.Logout:
    return lifespan.cases.employees.create_logout_case()


def get_refresh_token(
    cookies: Annotated[IAuthCookieManager, Depends(get_auth_cookie_manager)],
) -> str:
    return cookies.refresh_token


def get_refresh_case(
    lifespan: Annotated[LifespanState, Depends(get_lifespan_state)],
) -> cases.Refresh:
    return lifespan.cases.employees.create_refresh_case()


def get_system_headers_manager(
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
    headers: Annotated[ISystemHeaderManager, Depends(get_system_headers_manager)],
) -> str:
    return headers.user_agent

def get_ip_address(
    headers: Annotated[ISystemHeaderManager, Depends(get_system_headers_manager)],
) -> str:
    return headers.ip_address
