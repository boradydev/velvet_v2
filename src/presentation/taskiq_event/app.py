import dotenv
from taskiq import TaskiqEvents, TaskiqState

from src.core.logger import get_logger
from src.infrastructure.auth.jwt.token_service import JwtTokensService
from src.infrastructure.common.resources import AppState, Settings
from src.infrastructure.db.postgres.database import Postgres
from src.infrastructure.email.smtp import EmailService
from src.infrastructure.factories.cases.common import UseCaseResources
from src.infrastructure.message_brokers.rabbit_mq.publisher import RabbitMQPublisher
from src.infrastructure.security.codes import ConfirmCodeService
from src.infrastructure.security.password import PasswordService
from src.infrastructure.tasks.task_iq.broker_factory import get_broker


dotenv.load_dotenv()
settings = Settings()

broker = get_broker(
    url=settings.event_consumer.AMQP_URL,
    exchange_name=settings.event_consumer.EVENT_BROKER_EXCHANGE,
    queue_name=settings.event_consumer.EVENT_BROKER_QUEUE,
)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup_event(state: TaskiqState):
    logger = get_logger()
    postgres = Postgres(settings.postgres.DB_URL_ASYNC)
    event_publisher = RabbitMQPublisher(
        url=settings.event_publisher.AMQP_URL,
        exchange_name=settings.event_publisher.EVENT_BROKER_EXCHANGE,
    )
    interactor_resources = UseCaseResources(
        session_factory=postgres.session_factory,
        token_service=JwtTokensService(settings.jwt),
        password_service=PasswordService(settings.password.DEFAULT_CONTEXT),
        confirm_code_service=ConfirmCodeService(),
        email_service=EmailService(),
        logger=logger,
        event_publisher=event_publisher,
    )
    state.resources = AppState(
        settings=settings,
        interactors=interactor_resources,
        logger=logger,
    )


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown_event(state: TaskiqState):
    pass
