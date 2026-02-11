from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.auth.jwt.token_service import JwtTokensService
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
    postgres = Postgres(settings.postgres.DB_URL_ASYNC)
    interactor_resources = InteractorResources(
        session_factory=postgres.session_factory,
        token_service=JwtTokensService(settings.jwt),
        password_service=PasswordService(settings.password.DEFAULT_CONTEXT),
        confirm_code_service=ConfirmCodeService(),
        email_service=EmailService(),
    )
    app.state.resources = AppResources(
        settings=settings,
        interactors=interactor_resources,
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
