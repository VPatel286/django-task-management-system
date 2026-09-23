import logging

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Task


logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def process_task(self, task_id):
    try:
        logger.info("Processing task %s", task_id)

        return {
            "task_id": task_id,
            "status": "processed",
        }

    except Exception as exc:
        logger.error(
            "Task %s failed: %s",
            task_id,
            exc,
            exc_info=True,
        )

        raise self.retry(
            exc=exc,
            countdown=5,
        )


@shared_task(bind=True, max_retries=3)
def send_task_email(self, recipient_email, task_id):
    try:
        task = Task.objects.select_related("owner").get(id=task_id)

        logger.info(
            "Sending task email to %s for task '%s'",
            recipient_email,
            task.title,
        )

        context = {
            "user_name": task.owner.username,
            "task_id": task.id,
            "task_title": task.title,
            "task_description": task.description,
            "task_status": task.status,
            "completed": task.completed,
        }

        text_content = render_to_string(
            "task_api/emails/task_created.txt",
            context,
        )

        html_content = render_to_string(
            "task_api/emails/task_created.html",
            context,
        )

        email = EmailMultiAlternatives(
            subject="Task Created Successfully",
            body=text_content,
            from_email=None,
            to=[recipient_email],
        )

        email.attach_alternative(
            html_content,
            "text/html",
        )

        email.send()

        logger.info(
            "Task email sent successfully to %s",
            recipient_email,
        )

        return {
            "recipient": recipient_email,
            "task_id": task.id,
            "task_title": task.title,
            "status": "email_sent",
        }

    except Task.DoesNotExist as exc:
        logger.error(
            "Task %s does not exist",
            task_id,
        )

        raise self.retry(
            exc=exc,
            countdown=5,
        )

    except Exception as exc:
        logger.error(
            "Email task failed for %s: %s",
            recipient_email,
            exc,
            exc_info=True,
        )

        raise self.retry(
            exc=exc,
            countdown=5,
        )


@shared_task(bind=True, max_retries=3)
def send_task_reminders(self):
    try:
        incomplete_tasks = (
            Task.objects
            .filter(completed=False)
            .select_related("owner")
        )

        reminder_count = 0

        for task in incomplete_tasks:
            if not task.owner.email:
                logger.warning(
                    "Skipping reminder for task %s because "
                    "user %s has no email address.",
                    task.id,
                    task.owner.username,
                )
                continue

            context = {
                "user_name": task.owner.username,
                "task_id": task.id,
                "task_title": task.title,
                "task_description": task.description,
                "task_status": task.status,
                "completed": task.completed,
            }

            text_content = render_to_string(
                "task_api/emails/task_reminder.txt",
                context,
            )

            html_content = render_to_string(
                "task_api/emails/task_reminder.html",
                context,
            )

            email = EmailMultiAlternatives(
                subject=f"Task Reminder: {task.title}",
                body=text_content,
                from_email=None,
                to=[task.owner.email],
                cc=["sanuj@technmanconsulting.com"],
            )

            email.attach_alternative(
                html_content,
                "text/html",
            )

            email.send()

            reminder_count += 1

            logger.info(
                "Reminder email sent for task %s to %s",
                task.id,
                task.owner.email,
            )

        logger.info(
            "Task reminder job completed. "
            "Reminders sent: %s",
            reminder_count,
        )

        return {
            "reminders_sent": reminder_count,
            "status": "completed",
        }

    except Exception as exc:
        logger.error(
            "Task reminder job failed: %s",
            exc,
            exc_info=True,
        )

        raise self.retry(
            exc=exc,
            countdown=60,
        )
