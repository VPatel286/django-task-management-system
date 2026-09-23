import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.conf.timezone = "America/Toronto"
app.conf.enable_utc = True

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

app.autodiscover_tasks()


app.conf.beat_schedule = {
    "send-task-reminders-daily": {
        "task": "task_api.tasks.send_task_reminders",
        "schedule": crontab(
            hour=9,
            minute=0,
        ),
    },
}