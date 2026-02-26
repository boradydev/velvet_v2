import re
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Final

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

    PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(
        r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    )

    def __post_init__(self):
        object.__setattr__(self, "value", self.value.strip().lower())
        if not self.PATTERN.match(self.value):
            raise excs.InvalidEmailException

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class Password:
    r"""
    Валидирует сложность пароля.

    Использует флаг re.DOTALL: точка (.) совпадает с любым символом, включая \n.

    ``^`` - начало строки.

    ``(?=.*[A-Z])`` - проверка (lookahead) наличия хотя бы одной заглавной буквы.

    ``(?=.*[a-z])`` - проверка наличия хотя бы одной строчной буквы.

    ``(?=.*[0-9])`` - проверка наличия хотя бы одной цифры.

    ``(?=.*[!@#$%^&*(),.?":{}|<>])`` - проверка наличия минимум одного спецсимвола.

    ``.+$`` - пароль должен содержать минимум один любой символ до конца строки.
    """

    value: str = field(repr=False)

    MIN_LEN: ClassVar[int] = 8
    PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*(),.?\":{}|<>]).+$",
        re.DOTALL,
    )

    def __post_init__(self):
        if len(self.value) < self.MIN_LEN:
            raise excs.InvalidPasswordException

        if not self.PATTERN.match(self.value):
            raise excs.InvalidPasswordException


@dataclass(frozen=True, slots=True)
class ConfirmationCode:
    value: str

    PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^\d{6}$")

    def __post_init__(self):
        if not self.PATTERN.match(self.value):
            raise excs.InvalidConfirmationCodeException

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class PasswordHash:
    value: str = field(repr=False)

    MIN_LEN: ClassVar[Final[int]] = 30
    PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^\$.+$")

    def __post_init__(self):
        if len(self.value) < self.MIN_LEN:
            raise excs.InvalidPasswordHashException

        if not self.PATTERN.match(self.value):
            raise excs.InvalidPasswordHashException

        if " " in self.value:
            raise excs.InvalidPasswordHashException


@dataclass(frozen=True, slots=True)
class RoleName:
    """
    Нормализует строку, обрезает пробелы и приводит в нижний регистр.

    Разрешает: латиницу, цифры и нижнее подчеркивание.
    Не разрешает: пробелы, спецсимволы, пустые строки.

    ``^[a-z]`` - начинается строго с маленькой латинской буквы

    ``[a-z0-9_]*`` - далее любые латинские буквы, цифры или подчеркивание

    ``{2,19}`` - от 3 до 20 символов

    ``$`` - до конца строки
    """

    value: str

    MIN_LEN: ClassVar[Final[int]] = 3
    MAX_LEN: ClassVar[Final[int]] = 20
    PATTERN: ClassVar[Final[re.Pattern[str]]] = re.compile(r"^[a-z][a-z0-9_]{2,19}$")

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", self.value.strip().lower())
        has_len_range = self.MIN_LEN <= len(self.value) <= self.MAX_LEN
        has_pattern = self.PATTERN.match(self.value)
        if not has_len_range or not has_pattern:
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
