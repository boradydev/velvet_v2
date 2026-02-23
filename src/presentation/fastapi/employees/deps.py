from typing import Annotated

from fastapi import Depends, Request, Response

from src.application.employees import cases
from src.infrastructure.common.resources import AppState, LifespanState
from src.infrastructure.web.fastapi.cookies import AuthCookieManager
from src.presentation.fastapi.common.common_deps import get_lifespan_state


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
) -> AuthCookieManager:
    return AuthCookieManager(
        request=request,
        response=response,
        settings=app_state.settings.jwt,
    )
