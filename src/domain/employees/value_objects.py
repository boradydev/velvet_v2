import re
from dataclasses import dataclass
from enum import Enum

from src.domain.employees import exceptions


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise exceptions.InvalidEmailException


@dataclass(frozen=True, slots=True)
class PasswordHash:
    value: str

    def __post_init__(self):
        if len(self.value) < 8:
            raise exceptions.InvalidPasswordHashException


class EmployeeRole(str, Enum):
    OWNER = "owner"
    MANAGER = "manager"
    SALER = "saler"


class Permission(str, Enum):
    VIEW_PRODUCTS = "view_products"
    EDIT_PRODUCTS = "edit_products"

    GOODS_RECEIPT = "goods_receipt"
    REVALUATION = "revaluation"
    WRITE_OFF = "write_off"

    SALE = "sale"
    SALE_RETURN = "sale_return"

    SUPPLIER_RETURN = "supplier_return"
