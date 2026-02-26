import pytest
from hypothesis import given, settings, strategies as st

from src.domain.employees.excs import InvalidConfirmationCodeException
from src.domain.employees.vals import ConfirmationCode


@settings(max_examples=100)
@given(st.text(alphabet="0123456789", min_size=6, max_size=6))
def test_confirmation_code_accepts_valid_digits(valid_value):
    """Проверяет, что 6 цифр всегда проходят."""
    code = ConfirmationCode(valid_value)
    assert code.value == valid_value
    assert len(code.value) == 6
    assert str(code) == valid_value


@settings(max_examples=500)
@given(st.text())
def test_confirmation_code_rejects_garbage(garbage):
    """Проверяет, что всё, что не является 6 цифрами, отсекается."""
    if not ConfirmationCode.PATTERN.match(garbage):
        with pytest.raises(InvalidConfirmationCodeException):
            ConfirmationCode(garbage)


@pytest.mark.parametrize(
    "invalid",
    [
        "12345",
        "1234567",
        "abcdef",
        "123 56",
        " 123456",
    ],
)
def test_confirmation_code_manual_invalid(invalid):
    """Проверяет базовые негативные варианты."""
    with pytest.raises(InvalidConfirmationCodeException):
        ConfirmationCode(invalid)
