from collections.abc import Callable, Coroutine, Mapping
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.exceptions import BaseAppException
from src.core.logger import get_logger
from src.presentation.fastapi.base.schemas import ErrorResponse
from src.presentation.fastapi.base.types import Resp
from src.presentation.fastapi.employees.handlers import EMPLOYEE_EXCEPTION_MAP


def handle_unmapped_exception(exc: Exception) -> JSONResponse:
    """
    Логирует тип исключения и возвращает унифицированный ответ 500.

    Этот метод служит индикатором "пропущенного маппинга" в словаре исключений
    приложения (exception_map). Если бизнес-исключение (BaseAppException)
    не нашло своего соответствия в карте ответов, оно попадает сюда.

    Логирование:
        Используется краткая запись (Qualified Name класса ошибки), что позволяет
        быстро отследить, какое именно исключение забыли обработать в
        EMPLOYEE_EXCEPTION_MAP_VAR, не засоряя при этом лог избыточным Traceback.

    Returns:
        JSONResponse: Ответ 500, сигнализирующий о внутренней ошибке обработки.
    """
    error_path = f"{type(exc).__module__}.{type(exc).__name__}"
    get_logger().error("Unmapped exception caught: %s", error_path)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="Internal Server Error",
        ).model_dump(mode="json"),
    )


def get_business_exception_handler(
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
                    content=ErrorResponse(
                        detail=resp.detail,
                    ).model_dump(mode="json"),
                )

        return handle_unmapped_exception(exc)

    return handler


async def validation_exception_handler(_: Request, exc: Exception) -> JSONResponse:
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
            content=ErrorResponse(
                detail=str(exc.errors()),
            ).model_dump(mode="json"),
        )

    return handle_unmapped_exception(exc)


async def unknown_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """
    Обработчик непредвиденных системных исключений (500 Internal Server Error).

    Этот хендлер является "последним рубежом" обороны приложения. Он перехватывает
    любые ошибки, не относящиеся к бизнес-логике (например, KeyError, ValueError).

    Логирование:
        Используется параметр 'exc_info=True', который принудительно включает
        полный Traceback в лог. Это критически важно для дебага, так как позволяет
        точно определить файл и строку кода, где возникла ошибка, не раскрывая
        эти детали конечному пользователю.

    Returns:
        JSONResponse: Унифицированный ответ со статусом 500.
    """
    get_logger().error(exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="Internal Server Error",
        ).model_dump(mode="json"),
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрация глобальных обработчиков исключений для FastAPI."""
    app.add_exception_handler(
        BaseAppException, get_business_exception_handler(EMPLOYEE_EXCEPTION_MAP)
    )
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, unknown_exception_handler)
