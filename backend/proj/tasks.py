import time
import os

from .celery import app

# from backend.proj.celery import app

# test basic celery app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


@app.task(name="create_tas")
def create_task(task_type):
    time.sleep(int(task_type) * 3)
    # print(task_type)
    return True


hehe = "xinchao_variable"


@app.task(name=hehe)
def print_content(text):
    print(text)


###
from random import choice
import requests

mars_rover_url = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"


@app.task(name="mars photo")
def get_mars_photo(sol):
    params = {"sol": sol, "api_key": "tb9aFWsBVejrzbWLEZRWij20gPSGQi5MbnNC9BOS"}
    response = requests.get(mars_rover_url, params).json()
    photos = response["photos"]

    image = choice(photos)["img_src"]
    print(image)


###
# dynamically task #chưa dùng
PLUGIN_FOLDER = os.path.join(os.path.dirname(__file__), "tasks")


def _absolutepath(filename):
    """Return the absolute path to the filename"""
    return os.path.join(PLUGIN_FOLDER, filename)


@app.task
def tasks(funcname, *args, **kwargs):
    try:
        funcname = funcname.replace("-", "_")
        funcname += ".py"
        func = _absolutepath(funcname)
        ns = {}
        with open(func) as f:
            code = compile(f.read(), func, "exec")
            eval(code, ns, ns)
        return ns["task"](*args, **kwargs)
    except IOError as e:
        # Manage IOError
        raise e
