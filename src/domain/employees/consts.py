from enum import Enum

from src.domain.employees.vals import PermissionName


class Permissions(Enum):
    MANAGE_ROLES = PermissionName("manage_roles")
