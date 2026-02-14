from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.logger import get_logger
from src.infrastructure.auth.jwt.token_service import JwtTokensService
from src.infrastructure.brokers.rabbit_mq.client import RabbitMQEventBus
from src.infrastructure.db.postgres.database import Postgres
from src.infrastructure.email.smtp import EmailService
from src.infrastructure.factories.interactors.base import InteractorResources
from src.infrastructure.security.codes import ConfirmCodeService
from src.infrastructure.security.password import PasswordService
from src.presentation.fastapi.base import routers
from src.presentation.fastapi.base.dependencies import (
    AppResources,
    Settings,
)
from src.presentation.fastapi.base.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управляет жизненным циклом ресурсов приложения."""
    settings = Settings()
    logger = get_logger()
    postgres = Postgres(settings.postgres.DB_URL_ASYNC)
    event_bus = RabbitMQEventBus(
        url=settings.event_bus.AMQP_URL,
        exchange_name=settings.event_bus.DOMAIN_EVENTS_EXCHANGE
    )
    interactor_resources = InteractorResources(
        session_factory=postgres.session_factory,
        token_service=JwtTokensService(settings.jwt),
        password_service=PasswordService(settings.password.DEFAULT_CONTEXT),
        confirm_code_service=ConfirmCodeService(),
        email_service=EmailService(),
        logger=logger,
        event_bus=event_bus
    )
    app.state.resources = AppResources(
        settings=settings,
        interactors=interactor_resources,
        logger=logger,
    )
    app.root_path = settings.app.ROOT_PATH
    yield
    await postgres.dispose()


def fastapi_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    register_exception_handlers(app)
    app.include_router(routers.public)
    app.include_router(routers.protected)
    return app
