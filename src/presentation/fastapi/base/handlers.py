from collections.abc import Callable, Coroutine, Mapping
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.exceptions import BaseAppException
from src.presentation.fastapi.base.types import Resp
from src.presentation.fastapi.employees.handlers import EMPLOYEE_EXCEPTION_MAP_VAR


def internal_error_response(exc: Exception) -> JSONResponse:
    """Логирует и возвращает стандартный ответ при системной ошибке (500)."""
    # todo logger.error(exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Error"},
    )


def app_handler(
    exception_map: Mapping[type[BaseAppException], Resp],
) -> Callable[..., Coroutine[Any, Any, JSONResponse]]:
    """
    Создает универсальный асинхронный обработчик для исключений приложения.

    Функция реализует маппинг внутренних исключений (BaseAppException) в HTTP-ответы
    на основе предоставленной карты соответствий. Если исключение является частью
    бизнес-логики, возвращается JSONResponse с параметрами из exception_map.
    В случае системной ошибки или отсутствия маппинга (KeyError) возвращается
        500 статус.

    Args:
        exception_map: Словарь, сопоставляющий классы исключений их
            HTTP-представлениям (Resp).

    Returns:
        Callable: Асинхронная функция-обработчик, совместимая с интерфейсом FastAPI.
    """

    async def handler(_: Request, exc: Exception) -> JSONResponse:
        if isinstance(exc, BaseAppException):
            resp = exception_map.get(type(exc))
            if resp:
                return JSONResponse(
                    status_code=resp.status_code,
                    content={
                        "detail": resp.detail,
                    },
                )

        return internal_error_response(exc)

    return handler


async def pydantic_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Обработчик исключений валидации Pydantic (RequestValidationError).

    Принимает системную ошибку валидации FastAPI/Pydantic и трансформирует её
    в унифицированный формат ответа приложения. Использует проверку isinstance
    для обеспечения типизации и безопасности в рантайме.

    Args:
        _: Объект запроса (не используется, но требуется сигнатурой FastAPI).
        exc: Выброшенное исключение (ожидается RequestValidationError).

    Returns:
        JSONResponse: Ответ со статусом 422 и деталями валидации или
            500 при несоответствии типа.
    """
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )

    return internal_error_response(exc)


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрация глобальных обработчиков исключений для FastAPI."""
    app.add_exception_handler(BaseAppException, app_handler(EMPLOYEE_EXCEPTION_MAP_VAR))
    app.add_exception_handler(RequestValidationError, pydantic_handler)
