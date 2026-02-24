import pytest

from tests.unit.application.employees.fake_uow import FakeEmployeeUOW


@pytest.fixture
def employee_uow():
    return FakeEmployeeUOW()
