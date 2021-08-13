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
    ],
)

# Optional configuration, see the application user guide.
app.conf.update(result_expires=3600, timezone=CELERY_TIMEZONE)

# app.conf.CELERY_WORKER_SEND_TASK_EVENTS = True
# app.conf.timezone = CELERY_TIMEZONE

# celery beat
# test = 10
# app.conf.beat_schedule = {
#     # Executes every Monday morning at 7:30 a.m.
#     'run-every-Monday': {
#         'task': 'proj.tasks.add',
#         'schedule': crontab(hour=7, minute=30, day_of_week=1),
#         'args': (1,2),
#     },
#     'run-every-1min': {
#         'task': 'proj.tasks.xsum',
#         'schedule': test,
#         'args': ([3,4,5,6],),
#     },
#     'run-every-30s': {
#         'task': 'proj.tasks.mul',
#         'schedule': crontab(minute='*/1'),
#         'args': (3,4),
#     },
# }

if __name__ == "__main__":
    app.start()
