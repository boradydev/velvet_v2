from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from src.core.exceptions import BaseAppException
from src.core.logger import get_logger
from src.infrastructure.common.resources import AppState, Settings
from src.presentation.fastapi.base import handlers, routers
from src.presentation.fastapi.employees.handlers import EMPLOYEE_EXCEPTION_MAP
from src.presentation.fastapi.lifespan import lifespan


def fastapi_app() -> FastAPI:
    settings = Settings()
    logger = get_logger()

    app = FastAPI(lifespan=lifespan)
    app.state.app_state = AppState(
        settings=settings,
        logger=logger,
    )
    app.root_path = settings.app.ROOT_PATH

    app.add_exception_handler(
        BaseAppException,
        handlers.get_business_exception_handler(EMPLOYEE_EXCEPTION_MAP),
    )
    app.add_exception_handler(
        RequestValidationError,
        handlers.validation_exception_handler,
    )
    app.add_exception_handler(
        Exception,
        handlers.get_unknown_exception_handler(logger=logger, debug=settings.app.debug),
    )

    app.include_router(routers.public)
    app.include_router(routers.protected)
    return app
