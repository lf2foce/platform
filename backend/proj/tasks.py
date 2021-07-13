from .celery import app
import time

@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)

@app.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True    