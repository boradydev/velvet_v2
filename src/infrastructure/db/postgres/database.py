from collections.abc import Callable

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Postgres:
    """
    Управляет жизненным циклом подключений к базе данных PostgreSQL.

    Этот класс инкапсулирует создание асинхронного движка (Engine) и фабрики
    сессий, обеспечивая централизованное управление ресурсами БД.

    Attributes:
        _engine: Экземпляр асинхронного движка SQLAlchemy.
        session_factory : Фабрика для генерации
            новых асинхронных сессий.
    """

    _engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]

    def __init__(
        self,
        db_url: str,
        engine_factory: Callable[..., AsyncEngine] | None = None,
        session_factory_class: type[async_sessionmaker[AsyncSession]] | None = None,
    ) -> None:
        """
        Инициализирует PostgresDB и настраивает пул соединений.

        Args:
            db_url: URL подключения к базе данных.
            engine_factory: Функция для создания движка.
                По умолчанию create_async_engine.
            session_factory_class: Класс фабрики сессий.
                По умолчанию async_sessionmaker.
        """
        actual_engine_factory = engine_factory or create_async_engine
        self._engine = actual_engine_factory(db_url)
        actual_session_class = session_factory_class or async_sessionmaker
        self.session_factory = actual_session_class(
            bind=self._engine, expire_on_commit=False
        )

    async def dispose(self) -> None:
        """
        Закрывает все активные соединения в пуле движка.

        Должен вызываться при завершении работы приложения (например, в lifespan),
        чтобы избежать утечек соединений и ошибок "too many connections".
        """
        await self._engine.dispose()
