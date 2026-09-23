from unittest.mock import patch

from task_api.models import Task
from task_api.tasks import (
    process_task,
    send_task_email,
    send_task_reminders,
)


def test_process_task():
    result = process_task.run(123)

    assert result == {
        "task_id": 123,
        "status": "processed",
    }


@patch("task_api.tasks.EmailMultiAlternatives")
@patch("task_api.tasks.render_to_string")
def test_send_task_email(mock_render, mock_email, user):
    user.email = "test@example.com"
    user.save()

    task = Task.objects.create(
        title="Celery Email Test",
        description="Testing email task",
        completed=False,
        owner=user,
    )

    mock_render.side_effect = [
        "Text email content",
        "<p>HTML email content</p>",
    ]

    email_instance = mock_email.return_value

    result = send_task_email.run(
        "test@example.com",
        task.id,
    )

    assert result == {
        "recipient": "test@example.com",
        "task_id": task.id,
        "task_title": "Celery Email Test",
        "status": "email_sent",
    }

    mock_email.assert_called_once()

    email_instance.attach_alternative.assert_called_once_with(
        "<p>HTML email content</p>",
        "text/html",
    )

    email_instance.send.assert_called_once()


@patch("task_api.tasks.EmailMultiAlternatives")
@patch("task_api.tasks.render_to_string")
def test_send_task_reminders(mock_render, mock_email, user):
    user.email = "test@example.com"
    user.save()

    Task.objects.create(
        title="Incomplete Task 1",
        description="First incomplete task",
        completed=False,
        owner=user,
    )

    Task.objects.create(
        title="Incomplete Task 2",
        description="Second incomplete task",
        completed=False,
        owner=user,
    )

    Task.objects.create(
        title="Completed Task",
        description="Should not receive reminder",
        completed=True,
        owner=user,
    )

    mock_render.side_effect = [
        "Reminder text 1",
        "<p>Reminder HTML 1</p>",
        "Reminder text 2",
        "<p>Reminder HTML 2</p>",
    ]

    result = send_task_reminders.run()

    assert result == {
        "reminders_sent": 2,
        "status": "completed",
    }

    assert mock_email.call_count == 2

    for call in mock_email.call_args_list:
        assert call.kwargs["to"] == ["test@example.com"]
        assert call.kwargs["cc"] == [
            "sanuj@technmanconsulting.com"
        ]

    assert mock_email.return_value.send.call_count == 2
