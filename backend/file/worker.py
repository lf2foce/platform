from celery import Celery
from celery.schedules import crontab
from backend.config import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
    CELERY_TIMEZONE,
)

app = Celery(
    "proj",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "backend.proj.tasks",
        "backend.proj.service",
        "backend.team_projects.example.celery_example.service",
        "backend.notification.service",
        "backend.job.service",
    ],
)

# Optional configuration, see the application user guide.
app.conf.update(result_expires=3600, timezone=CELERY_TIMEZONE, result_extended=True)

# app.conf.CELERY_WORKER_SEND_TASK_EVENTS = True
# app.conf.timezone = CELERY_TIMEZONE


if __name__ == "__main__":
    app.start()
