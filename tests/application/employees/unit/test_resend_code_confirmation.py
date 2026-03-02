from datetime import datetime, timedelta

import pytest

from src.application.employees import excs
from src.domain.employees.entities import Registration
from src.domain.employees.events import ConfirmationCodeResentEvent
from src.domain.employees.vals import ConfirmationCode


async def test_resend_confirmation_success(
    resend_use_case,
    resend_confirmation_code_dto,
    mock_registration_repo,
    mock_code_service,
    mock_event_publisher,
    mock_registration_policy,
    get_registration_entity,
    mock_now,
) -> None:
    dto = resend_confirmation_code_dto
    new_code = ConfirmationCode("000000")

    now: datetime = mock_now()
    registration_time = now - timedelta(minutes=10)
    confirmation_ttl = timedelta(minutes=30)
    min_resend_ttl = timedelta(minutes=2)
    cooldown = timedelta(minutes=1)

    mock_now.return_value = registration_time
    mock_registration_policy.get_min_resend_ttl.return_value = min_resend_ttl
    mock_registration_policy.get_cooldown.return_value = cooldown
    mock_registration_policy.get_confirmation_ttl.return_value = confirmation_ttl

    registration = get_registration_entity()
    registration._events.clear()
    mock_registration_repo.get_by_email.return_value = registration
    mock_code_service.generate.return_value = new_code
    mock_now.return_value = now

    assert registration.resend_count == 0
    assert registration.confirmation_code != new_code

    await resend_use_case.execute(dto=resend_confirmation_code_dto)

    repo_kwargs = mock_registration_repo.save_if_version_matches.call_args.kwargs
    save_registration: Registration = repo_kwargs["dto"]
    assert save_registration.resend_count == 1
    assert save_registration.confirmation_code == new_code
    assert len(save_registration._events) == 0
    assert save_registration.last_code_sent_at == now
    expected_ttl = confirmation_ttl - (now - registration_time)
    assert repo_kwargs["ttl"] == expected_ttl
    assert repo_kwargs["ttl"] < confirmation_ttl

    mock_code_service.generate.assert_called_once()
    mock_registration_repo.get_by_email.assert_awaited_once_with(email=dto.email)
    mock_registration_repo.save_if_version_matches.assert_awaited_once()
    mock_event_publisher.publish_many.assert_awaited_once()

    event_kwargs = mock_event_publisher.publish_many.call_args.kwargs
    published_events: list[ConfirmationCodeResentEvent] = event_kwargs["events"]
    assert published_events[0].email == dto.email
    assert published_events[0].confirmation_code == new_code


async def test_resend_confirmation_fails_if_registration_not_found(
    resend_use_case,
    resend_confirmation_code_dto,
    mock_registration_repo,
    mock_event_publisher,
) -> None:
    mock_registration_repo.get_by_email.return_value = None

    with pytest.raises(excs.RegistrationNotFound):
        await resend_use_case.execute(dto=resend_confirmation_code_dto)

    mock_registration_repo.save_if_version_matches.assert_not_awaited()
    mock_event_publisher.publish_many.assert_not_awaited()


async def test_resend_confirmation_fails_if_too_late(
    resend_use_case,
    resend_confirmation_code_dto,
    mock_registration_repo,
    mock_event_publisher,
    mock_registration_policy,
    get_registration_entity,
    mock_now,
) -> None:
    now: datetime = mock_now()
    min_resend_ttl = timedelta(minutes=2)

    mock_registration_policy.get_min_resend_ttl.return_value = min_resend_ttl

    registration = get_registration_entity()
    registration.confirmation_deadline = now - timedelta(minutes=29)
    mock_registration_repo.get_by_email.return_value = registration

    with pytest.raises(excs.TooLateToResend):
        await resend_use_case.execute(dto=resend_confirmation_code_dto)

    mock_registration_repo.save_if_version_matches.assert_not_awaited()
    mock_event_publisher.publish_many.assert_not_awaited()


async def test_resend_confirmation_fails_if_cooldown_not_expired(
    resend_use_case,
    resend_confirmation_code_dto,
    mock_registration_repo,
    mock_event_publisher,
    mock_registration_policy,
    get_registration_entity,
    mock_now,
) -> None:
    now = mock_now()
    confirmation_ttl = timedelta(minutes=30)
    cooldown = timedelta(seconds=60)

    mock_registration_policy.get_confirmation_ttl.return_value = confirmation_ttl
    mock_registration_policy.get_cooldown.return_value = cooldown
    mock_registration_policy.get_min_resend_ttl.return_value = timedelta(seconds=1)

    registration = get_registration_entity()
    registration.last_code_sent_at = now - timedelta(seconds=30)
    mock_registration_repo.get_by_email.return_value = registration

    with pytest.raises(excs.CooldownNotExpired):
        await resend_use_case.execute(dto=resend_confirmation_code_dto)

    mock_registration_repo.save_if_version_matches.assert_not_awaited()
    mock_event_publisher.publish_many.assert_not_awaited()
