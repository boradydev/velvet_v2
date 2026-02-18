"""
Инициализация брокера задач для TaskIQ.

Данный модуль отвечает за создание и конфигурацию центрального узла (брокера),
через который происходит регистрация и отправка фоновых задач.

Note:
    Использование глобальной переменной `tasks_broker` является архитектурной
    необходимостью TaskIQ по следующим причинам:

    1. Регистрация задач: Декоратор `@tasks_broker.task` должен быть доступен
       на этапе импорта модулей, чтобы воркер мог обнаружить и
       зарегистрировать функции-обработчики.
    2. Синхронизация путей: При сериализации задачи TaskIQ фиксирует путь к
       объекту брокера. Глобальная область видимости гарантирует, что
       отправитель (App) и исполнитель (Worker) используют идентичный
       идентификатор брокера.
    3. Singleton: Гарантирует создание единственного соединения с RabbitMQ
       в рамках процесса, предотвращая утечки ресурсов.

Attributes:
    tasks_broker (AioPikaBroker): Глобальный экземпляр брокера, используемый
        для декорирования задач и управления их жизненным циклом.
"""

import taskiq_aio_pika

from src.infrastructure.tasks.task_iq.broker_factory import get_broker
from src.infrastructure.tasks.task_iq.settings import TasksSettings


def get_tasks_broker() -> taskiq_aio_pika.AioPikaBroker:
    settings = TasksSettings()
    return get_broker(
        url=settings.AMQP_URL,
        exchange_name=settings.TASK_BROKER_EXCHANGE,
        queue_name=settings.TASK_BROKER_QUEUE,
    )


tasks_broker = get_tasks_broker()
