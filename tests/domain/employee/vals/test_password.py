import pytest
from hypothesis import given, settings, strategies as st

from src.domain.employees.excs import InvalidPasswordException
from src.domain.employees.vals import Password


valid_password_strategy = st.tuples(
    st.text(alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ", min_size=1),
    st.text(alphabet="abcdefghijklmnopqrstuvwxyz", min_size=1),
    st.text(alphabet="0123456789", min_size=1),
    st.text(alphabet='!@#$%^&*(),.?":{}|<>', min_size=1),
    st.text(min_size=4),
).map(lambda parts: "".join(parts))


@settings(max_examples=200)
@given(valid_password_strategy)
def test_password_accepts_valid_complex_input(valid_pw):
    """Проверяет, что верные пароли проходят валидацию."""
    pw = Password(valid_pw)
    assert valid_pw not in repr(pw)
    assert valid_pw not in str(pw)


@settings(max_examples=1000)
@given(st.text())
def test_password_rejects_random_garbage(garbage):
    """Проверяет, что случайный мусор не проходит."""
    if len(garbage) < Password.MIN_LEN or not Password.PATTERN.match(garbage):
        with pytest.raises(InvalidPasswordException):
            Password(garbage)


@pytest.mark.parametrize(
    "weak_pw",
    [
        "Short1!",
        "NoDigits!",
        "nouppercase1!",
        "NOLOWERCASE1!",
        "NoSpecial123",
    ],
)
def test_password_manual_weak_cases(weak_pw):
    """Проверка конкретных нарушений правил."""
    with pytest.raises(InvalidPasswordException):
        Password(weak_pw)
