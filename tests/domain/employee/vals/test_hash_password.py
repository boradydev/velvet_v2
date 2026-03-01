import pytest
from hypothesis import given, settings, strategies as st

from src.domain.employees.excs import InvalidPasswordHashException
from src.domain.employees.vals import PasswordHash


valid_hash_strategy = st.text(
    alphabet=st.characters(
        whitelist_categories=["Lu", "Ll", "Nd", "Pd", "Po"],
        min_codepoint=33,
        max_codepoint=126,
    ),
    min_size=30,
).map(lambda s: f"${s}")


@settings(max_examples=100)
@given(valid_hash_strategy)
def test_password_hash_accepts_valid_format(valid_h):
    """Проверяет, что строки формата '$...' проходят."""
    ph = PasswordHash(valid_h)
    assert ph.value == valid_h


@settings(max_examples=500)
@given(st.text())
def test_password_hash_rejects_garbage(garbage):
    """Проверяет, что случайный текст без $ или короткий — отсекается."""
    if (
        not garbage.startswith("$")
        or len(garbage) < PasswordHash.MIN_LEN
        or " " in garbage
    ):
        with pytest.raises(InvalidPasswordHashException):
            PasswordHash(garbage)


def test_password_hash_repr_is_hidden():
    """Проверяет, что repr=False работает (хэш не светится в логах дата класса)."""
    ph = PasswordHash("$argon2id$v=19$m=65536,t=3,p=4$very_long_hash_string")
    assert "very_long_hash_string" not in repr(ph)
    assert "very_long_hash_string" not in str(ph)
