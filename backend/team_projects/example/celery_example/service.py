import logging
import time
from celery import Task
from backend.proj.celery import app as celery_app


@celery_app.task()
def create_task2():
    time.sleep(2)

    return True
