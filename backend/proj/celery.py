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

# test beat
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls train_model('data-set-a') every 10 seconds.
#     sender.add_periodic_task(10.0, train_model.s("data-set-a"), name="add every 10")

#     # Calls train_model('data-set-b') every 30 seconds
#     sender.add_periodic_task(30.0, train_model.s("data-set-b"), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         train_model.s("data-set-c"),
#     )


# @app.task
# def train_model(args):
#     print("dask train model in progress...{}".format(args))

##

if __name__ == "__main__":
    app.start()
