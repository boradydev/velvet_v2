from src.domain.common.consts import SystemRoles
from src.domain.employees.entities import Employee
from src.domain.employees.excs import PermissionDeniedException
from src.domain.employees.interfaces.policies import IAuthorizationPolicy
from src.domain.employees.vals import PermissionName, RoleName


class AuthorizationPolicy(IAuthorizationPolicy):

    def ensure_can(
        self,
        employee: Employee,
        permission: PermissionName,
    ) -> None:
        if permission not in employee.permission_names:
            raise PermissionDeniedException

    def get_default_role(self) -> RoleName:
        return SystemRoles.SELLER.value

    def get_owner_role(self) -> RoleName:
        return SystemRoles.OWNER.value
