from task_api.models import Task
from task_api.services import TaskService
from unittest.mock import patch


def test_create_task(user):
    task = TaskService.create_task(
        validated_data={
            "title": "Service Test Task",
            "description": "Created directly through service",
            "completed": False,
        },
        owner=user,
    )

    assert task.title == "Service Test Task"
    assert task.owner == user
    assert Task.objects.filter(id=task.id).exists()


def test_update_task(user):
    task = TaskService.create_task(
        validated_data={
            "title": "Original Title",
            "description": "Original description",
            "completed": False,
        },
        owner=user,
    )

    updated_task = TaskService.update_task(
        task=task,
        validated_data={
            "title": "Updated Title",
            "completed": True,
        },
    )

    assert updated_task.title == "Updated Title"
    assert updated_task.completed is True


def test_delete_task(user):
    task = TaskService.create_task(
        validated_data={
            "title": "Task To Delete",
            "description": "This task will be deleted",
            "completed": False,
        },
        owner=user,
    )

    TaskService.delete_task(task=task)

    assert not Task.objects.filter(id=task.id).exists()


def test_create_task_calls_database_create(user):
    with patch("task_api.services.Task.objects.create") as mock_create:
        TaskService.create_task(
            validated_data={
                "title": "Mocked Task",
                "description": "Testing mock",
                "completed": False,
            },
            owner=user,
        )

        mock_create.assert_called_once_with(
            owner=user,
            title="Mocked Task",
            description="Testing mock",
            completed=False,
        )


def test_update_task_tags(user):
    from task_api.models import Tag

    task = TaskService.create_task(
        validated_data={
            "title": "Tag Update Test",
            "description": "Testing tag updates",
            "completed": False,
        },
        owner=user,
    )

    tag1 = Tag.objects.create(name="Backend")
    tag2 = Tag.objects.create(name="Celery")

    updated_task = TaskService.update_task(
        task=task,
        validated_data={
            "tags": [tag1, tag2],
        },
    )

    assert set(updated_task.tags.all()) == {tag1, tag2}
