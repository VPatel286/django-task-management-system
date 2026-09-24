from django.tasks import task

from .models import Tag, Task


class TaskService:

    @staticmethod
    def create_task(*, validated_data, owner):
        tags = validated_data.pop("tags", [])

        task = Task.objects.create(
            owner=owner,
            **validated_data,
        )

        if tags:
            task.tags.set(tags)

        return task

    @staticmethod
    def update_task(*, task, validated_data):
        tags = validated_data.pop("tags", None)

        for field, value in validated_data.items():
            setattr(task, field, value)

        task.save()

        if tags is not None:
            task.tags.set(tags)

        return task
    @staticmethod
    def delete_task(*, task):
        task.delete()


