import pytest
from hypothesis import given, settings, strategies as st

from src.domain.employees.excs import InvalidRoleNameException
from src.domain.employees.vals import RoleName


valid_role_strategy = st.from_regex(RoleName._PATTERN, fullmatch=True).filter(
    lambda s: RoleName._MIN_LEN <= len(s) <= RoleName._MAX_LEN
)


@settings(max_examples=100)
@given(valid_role_strategy)
def test_role_name_accepts_valid_input(valid_val):
    """Проверяем, что снэк кейс и латиница проходят."""
    role = RoleName(valid_val)
    assert role.value == valid_val.lower()
    assert str(role) == valid_val.lower()


def test_role_name_normalization():
    """Проверяем strip и lower."""
    role = RoleName("  ADMIN_User  ")
    assert role.value == "admin_user"


@settings(max_examples=500)
@given(st.text())
def test_role_name_rejects_garbage(garbage):
    """Проверяем, что любой невалидный формат отсекается."""
    processed = garbage.strip().lower()
    if not RoleName._PATTERN.match(processed) or len(processed) > RoleName._MAX_LEN:
        with pytest.raises(InvalidRoleNameException):
            RoleName(garbage)


@pytest.mark.parametrize(
    "invalid_role",
    [
        "1admin",
        "_user",
        "admin role",
        "admin-role",
        "a" * 21,
        "",
        "   ",
        "role!",
    ],
)
def test_role_name_manual_invalid(invalid_role):
    with pytest.raises(InvalidRoleNameException):
        RoleName(invalid_role)
