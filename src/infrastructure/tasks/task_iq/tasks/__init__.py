"""
Пакет фоновых задач (Worker Side).

Данный пакет объединяет все модули задач TaskIQ, выполняемых асинхронно
через брокер сообщений RabbitMQ. Служит единой точкой входа для воркера.

Архитектура DTO Transfer:
    Задачи используют принцип прозрачного переноса объектов данных (DTO):

    1. Producer (App): При вызове `.kiq(dto)` dataclass сериализуется в JSON.
    2. Broker (RabbitMQ): Хранит сообщение, сохраняя структуру полей DTO.
    3. Consumer (Worker): TaskIQ восстанавливает (инстанциирует) объект DTO
       на основе аннотаций типов функции перед её выполнением.

Структура пакета:
    - .broker: Инициализация и конфигурация `tasks_broker`.
    - .employees: Задачи домена сотрудников (уведомления, коды).
    - .orders: Задачи домена заказов (если применимо).

Note:
    Для корректной десериализации все DTO должны импортироваться по
    абсолютным путям, идентичным в App и Worker (например, `src.application...`).

Example:
    Запуск воркера для данного пакета:
    $ taskiq_event worker src.infrastructure.tasks:tasks_broker
"""

from src.infrastructure.tasks.task_iq.tasks import employees as employees
