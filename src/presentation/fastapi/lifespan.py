from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.auth.jwt.token_service import JwtTokensService
from src.infrastructure.common.resources import AppState, LifespanState
from src.infrastructure.db.postgres.database import Postgres
from src.infrastructure.email.smtp import EmailService
from src.infrastructure.factories.interactors.base import InteractorResources
from src.infrastructure.message_brokers.rabbit_mq.publisher import RabbitMQPublisher
from src.infrastructure.security.codes import ConfirmCodeService
from src.infrastructure.security.password import PasswordService
from src.infrastructure.tasks.task_iq.tasks.broker import tasks_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управляет жизненным циклом ресурсов приложения."""
    app_state: AppState = app.state.app_state
    settings = app_state.settings
    logger = app_state.logger
    postgres = Postgres(settings.postgres.DB_URL_ASYNC)
    event_publisher = RabbitMQPublisher(
        url=settings.event_publisher.AMQP_URL,
        exchange_name=settings.event_publisher.EVENT_BROKER_EXCHANGE,
    )
    interactor_resources = InteractorResources(
        session_factory=postgres.session_factory,
        token_service=JwtTokensService(settings.jwt),
        password_service=PasswordService(settings.password.DEFAULT_CONTEXT),
        confirm_code_service=ConfirmCodeService(),
        email_service=EmailService(),
        logger=logger,
        event_publisher=event_publisher,
    )
    app.state.lifespan_state = LifespanState(
        interactors=interactor_resources,
        tasks_broker=tasks_broker,
    )
    yield
    await postgres.dispose()
