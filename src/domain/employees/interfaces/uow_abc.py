from abc import ABC

from src.domain.common.interfaces.uow_abc import InterfaceUOW
from src.domain.employees.interfaces.repos import db_abc


class IEmployeeUOW(InterfaceUOW, ABC):
    """
    Интерфейс Unit of Work для управления транзакциями данных сотрудников.

    Attributes:
        employees: Требует репозиторий для сотрудников.
        auth_sessions: Требует репозиторий для сессий аутентификации.
    """

    employees: db_abc.IEmployeeRepository
    auth_sessions: db_abc.IAuthSessionsRepository
