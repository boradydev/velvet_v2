from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.application.auth import interactors
from src.infrastructure.db.postgres.repositories.employees import EmployeeRepository
from src.infrastructure.db.postgres.uow.uow import EmployeeUOW
from src.infrastructure.email.smtp import EmailService
from src.infrastructure.security.codes import ConfirmationCodeService
from src.infrastructure.security.password import PasswordService
from src.presentation.fastapi.base.dependencies import (
    get_db_session_factory,
    get_password_service,
)


async def get_register_interactor(
    session_factory: Annotated[
        async_sessionmaker[AsyncSession], Depends(get_db_session_factory)
    ],
    password_service: Annotated[PasswordService, Depends(get_password_service)],
    confirm_code_service: Annotated[ConfirmationCodeService, Depends()],
    email_service: Annotated[EmailService, Depends()],
) -> interactors.RegisterInteractor:
    """
    Провайдер для сборки и инициализации интерактора регистрации.

    Выполняет роль Composition Root (корня композиции), инкапсулируя процесс
    объединения инфраструктурных сервисов и Unit of Work в единый сценарий
    бизнес-логики.

    Args:
        session_factory: Фабрика асинхронных сессий SQLAlchemy для управления
            транзакциями БД.
        password_service: Сервис для работы с хешированием и проверкой паролей.
        confirm_code_service: Сервис генерации и валидации кодов подтверждения.
        email_service: Транспортный сервис для отправки почтовых уведомлений.

    Returns:
        RegisterInteractor: Полностью инициализированный экземпляр интерактора,
            готовый к выполнению бизнес-сценариев авторизации.

    Note:
        - Репозиторий EmployeeRepository внедряется в Unit of Work как класс (лениво),
          что предотвращает преждевременный захват соединений из пула.

        - Unit of Work (UOW) реализует протокол асинхронного контекстного менеджера
          (`async with`), обеспечивая атомарность (ACID) выполняемых операций.

        - Архитектура допускает существование множества специализированных UOW.
          Если бизнес-логика интерактора требует работы с несколькими сущностями
          в рамках одной транзакции, в провайдере собирается UOW, содержащий
          необходимый набор репозиториев.

        - Интерактор всегда использует конкретную реализацию UOW, наиболее
          подходящую для решения его задачи, что исключает создание
          избыточных "God-объектов".

        - В аргументы функции выносятся только внешние зависимости (сервисы, БД),
          требующие управления жизненным циклом или глобальной подмены в тестах.
          Сборка внутренних компонентов (UOW, Interactor) намеренно скрыта внутри
          тела функции, так как они являются деталями реализации конкретного
          сценария и не требуют избыточного вынесения в систему Depends FastAPI.
    """
    uow = EmployeeUOW(
        session_factory=session_factory,
        employee_repo_class=EmployeeRepository,
    )
    return interactors.RegisterInteractor(
        uow=uow,
        password_service=password_service,
        confirmation_code_service=confirm_code_service,
        send_email_service=email_service,
    )
