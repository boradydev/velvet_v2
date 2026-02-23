import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Final

from src.domain.employees import excs


@dataclass(frozen=True, slots=True)
class Email:
    r"""
    Обрезает пробелы по краям и приводит адрес к нижнему регистру.

    ``^[^\s@]+`` - начало строки, минимум один символ (кроме пробела и @)

    ``@`` - обязательный символ разделителя.

    ``[^\s@]+`` - имя домена (минимум один символ без пробелов и @).

    ``\.`` - обязательная точка в домене.

    ``[^\s@]+$`` - доменная зона.
    """

    value: str

    _PATTERN: Final = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")

    def __post_init__(self):
        object.__setattr__(self, "value", self.value.strip().lower())
        if not self._PATTERN.match(self.value):
            raise excs.InvalidEmailException

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class ConfirmationCode:
    value: str
    _LENGTH: Final = 6

    def __post_init__(self):
        if len(self.value) == self._LENGTH:
            raise excs.InvalidPasswordHashException

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class PasswordHash:
    value: str = field(repr=False)
    _MIN_LENGTH: Final = 8

    def __post_init__(self):
        if len(self.value) < self._MIN_LENGTH:
            raise excs.InvalidPasswordHashException


@dataclass(frozen=True, slots=True)
class RoleName:
    """
    Нормализует строку, обрезает пробелы и приводит в нижний регистр.

    Разрешает: латиницу, цифры и нижнее подчеркивание.
    Не разрешает: пробелы, спецсимволы, пустые строки.

    ``^[a-z]`` - начинается строго с маленькой латинской буквы

    ``[a-z0-9_]*`` - далее любые латинские буквы, цифры или подчеркивание

    ``$`` - до конца строки
    """

    value: str

    _MAX_LENGTH: Final[int] = 20
    _PATTERN: Final = re.compile(r"^[a-z][a-z0-9_]*$")

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self.value.strip().lower())
        if len(self.value) > self._MAX_LENGTH or not self._PATTERN.match(self.value):
            raise excs.InvalidRoleNameException

    def __str__(self) -> str:
        return self.value


class SystemRoles(Enum):
    OWNER = RoleName("owner")
    ADMIN = RoleName("admin")
    MANAGER = RoleName("manager")
    SELLER = RoleName("seller")


class Permission(str, Enum):
    VIEW_PRODUCTS = "view_products"
    EDIT_PRODUCTS = "edit_products"

    GOODS_RECEIPT = "goods_receipt"
    REVALUATION = "revaluation"
    WRITE_OFF = "write_off"

    SALE = "sale"
    SALE_RETURN = "sale_return"

    SUPPLIER_RETURN = "supplier_return"

    MANAGE_ROLES = "manage_roles"
