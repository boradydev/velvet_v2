import pytest
from hypothesis import given, settings, strategies as st

from src.domain.employees.excs import InvalidEmailException
from src.domain.employees.vals import Email


@pytest.mark.parametrize(
    "valid_email",
    [
        "test@example.com",
        "user.name+tag@sub.domain.org",
        "123@456.78",
    ],
)
def test_email_manual_positive(valid_email):
    """Проверяет базовые позитивные варианты."""
    email = Email(valid_email)
    assert email.value == valid_email.lower()


def test_email_strip_and_lower():
    """Проверяет очистку данных и строковое представление."""
    raw_input = "  CAPS@Domain.Com  "
    expected = "caps@domain.com"
    email = Email(raw_input)

    assert email.value == expected
    assert str(email) == expected


@settings(max_examples=200)
@given(st.emails())
def test_email_accepts_all_valid_hypothesis(valid_email):
    """Генерирует реально существующие форматы email."""
    Email(valid_email)


@settings(max_examples=500)
@given(st.text())
def test_email_rejects_random_garbage(garbage):
    """
    Проверяет, что VO не пропускает мусор.

    Если вдруг сгенерируется валидный email, условие его не пропустит.
    """
    if not Email._PATTERN.match(garbage.strip().lower()):
        with pytest.raises(InvalidEmailException):
            Email(garbage)
