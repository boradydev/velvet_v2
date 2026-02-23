from taskiq import TaskiqState

from src.infrastructure.common.resources import AppState


def get_resources(state: TaskiqState) -> AppState:
    """Извлекает ресурсы приложения из состояния Taskiq."""
    return state.resources
