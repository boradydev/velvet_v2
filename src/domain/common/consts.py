from enum import Enum

from src.domain.employees.vals import RoleName


class SystemRoles(Enum):
    OWNER = RoleName("owner")
    ADMIN = RoleName("admin")
    MANAGER = RoleName("manager")
    SELLER = RoleName("seller")
