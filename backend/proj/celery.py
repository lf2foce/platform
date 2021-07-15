
from celery import Celery
from celery.schedules import crontab

from config import (
    CELERY_BROKER_URL,
    CELERY_RESULT_BACKEND,
    CELERY_TIMEZONE,
)


app = Celery('proj',
             broker=CELERY_BROKER_URL,
             backend=CELERY_RESULT_BACKEND,
             include=['proj.tasks', 'team_projects.celery_example.service'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)
app.conf.timezone = CELERY_TIMEZONE

test = 10
app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'run-every-Monday': {
        'task': 'proj.tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (1,2),
    },
    'run-every-1min': {
        'task': 'proj.tasks.xsum',
        'schedule': test,
        'args': ([3,4,5,6],),
    },
    'run-every-30s': {
        'task': 'proj.tasks.mul',
        'schedule': crontab(minute='*/1'),
        'args': (3,4),
    },
}


if __name__ == '__main__':
    app.start()