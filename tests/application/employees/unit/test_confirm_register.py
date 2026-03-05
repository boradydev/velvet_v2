from datetime import datetime, timedelta

from uuid6 import uuid7

from src.domain.auth_sessions.entity import AuthSession
from src.domain.common.events import BaseDomainEvent
from src.domain.employees.entities import Employee
from src.domain.employees.vals import RoleName


async def test_confirm_register_success(
    get_registration_entity,
    confirmation_registration_dto,
    use_case_confirm_register,
    mock_employee_uow,
    mock_registration_repo,
    mock_token_service,
    mock_registration_policy,
    mock_id_generator,
    mock_now,
) -> None:
    now: datetime = mock_now()
    mock_registration_policy.get_confirmation_ttl.return_value = timedelta(minutes=30)
    default_role = RoleName("ROLE_USER")
    mock_registration_policy.get_default_role.return_value = default_role
    registration = get_registration_entity()

    mock_registration_repo.find_by_email.return_value = registration
    session_expires_at = now + timedelta(weeks=1)
    mock_registration_policy.get_refresh_session_expires_at.return_value = (
        session_expires_at
    )
    test_access_token = "access_val"
    test_refresh_token = "refresh_val"
    mock_token_service.create_access_token.return_value = test_access_token
    mock_token_service.create_refresh_token.return_value = test_refresh_token
    mock_employee_uow.__aenter__.return_value = mock_employee_uow
    dto = confirmation_registration_dto
    employee_id = uuid7()
    auth_session_id = uuid7()
    mock_id_generator.side_effect = [employee_id, auth_session_id]

    result = await use_case_confirm_register.execute(dto=dto)

    assert mock_id_generator.call_count == 2
    assert result.access_token == test_access_token
    assert result.refresh_token == test_refresh_token

    mock_employee_uow.employees.add.assert_called_once()
    mock_employee_uow.auth_sessions.save.assert_called_once()
    mock_registration_repo.delete_by_email.assert_awaited_once_with(
        email=confirmation_registration_dto.email
    )
    mock_employee_uow.commit.assert_awaited_once()

    event_kwargs = mock_employee_uow.commit.call_args.kwargs
    published_events: list[BaseDomainEvent] = event_kwargs["events"]
    assert len(published_events) > 0

    employee_add_kwargs = mock_employee_uow.employees.add.call_args.kwargs
    added_employee: Employee = employee_add_kwargs["employee"]
    assert added_employee.id == employee_id
    assert added_employee.email == dto.email
    assert default_role in added_employee.has_roles

    create_token_kwargs = mock_token_service.create_refresh_token.call_args.kwargs
    assert create_token_kwargs["employee_id"] == employee_id
    assert create_token_kwargs["session_id"] == auth_session_id

    auth_session_save_kwargs = mock_employee_uow.auth_sessions.save.call_args.kwargs
    saved_session: AuthSession = auth_session_save_kwargs["auth_session"]
    assert saved_session.expires_at == session_expires_at
    assert saved_session.employee_id == employee_id
    assert saved_session.id == auth_session_id
    assert saved_session.created_at == now
