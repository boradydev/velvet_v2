from src.application.employees import cases
from src.application.employees.interfaces import IEmployeeUseCaseResources
from src.infrastructure.db.postgres.repositories.employees import EmployeeRepository
from src.infrastructure.db.postgres.uow.uow import EmployeeUOW


class EmployeeUseCaseFactory:
    """
    Фабрика интеракторов для домена сотрудников.

    - Interface Segregation (ISP):
        Фабрика зависит от узкого интерфейса `IEmployeeInteractorResources`.
        Она не имеет доступа к лишним методам общего корня композиции.
    - Dependency Inversion (DIP): Класс зависит от абстракций.
    - Framework Agnostic: Фабрика не зависит от конкретного фреймворка(слой презентации)
    - Осознанное заземление (Infrastructure Binding):
        Использование конкретных классов `EmployeeUOW` и `EmployeeRepository`
        внутри методов является осознанным проектным решением. Это единственная
        точка, где инфраструктура ДБ «протекает» в логику сборки.
    """

    resources: IEmployeeUseCaseResources

    def __init__(self, resources: IEmployeeUseCaseResources) -> None:
        """
        Инициализирует фабрику через внедрение зависимости.

        Args:
            resources: Объект-провайдер, реализующий интерфейс ресурсов,
                          необходимых для создания интеракторов сотрудников.
        """
        self.resources = resources

    def create_register_case(self) -> cases.Register:
        """Создает сценарий регистрации нового сотрудника."""
        uow = EmployeeUOW(
            session_factory=self.resources.session_factory,
            employee_class=EmployeeRepository,
            event_publisher=self.resources.event_publisher,
        )

        return cases.Register(
            uow=uow,
            password_service=self.resources.password_service,
            logger=self.resources.logger,
        )

    def create_login_case(self) -> cases.Login:
        """Создает сценарий аутентификации сотрудника."""
        uow = EmployeeUOW(
            session_factory=self.resources.session_factory,
            employee_class=EmployeeRepository,
            event_publisher=self.resources.event_publisher,
        )
        return cases.Login(
            uow=uow,
            token_service=self.resources.token_service,
            password_service=self.resources.password_service,
            logger=self.resources.logger,
        )
