from fastapi.requests import Request

from src.infrastructure.common.resources import AppState, LifespanState


def get_app_state(request: Request) -> AppState:
    return request.app.state.app_state


def get_lifespan_state(request: Request) -> LifespanState:
    return request.app.state.lifespan_state
