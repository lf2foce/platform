import logging
import time
from celery import Task
from worker import celery

from proj.celery import app

@app.task()
def create_task2():
    time.sleep(2)
    return True