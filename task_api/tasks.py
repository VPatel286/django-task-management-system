import logging

from celery import shared_task


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
