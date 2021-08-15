import time
import os

from .celery import app


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


@app.task(name="create_task")
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


# print mars_photos
def print_mars_photos():
    for i in range(10):
        get_mars_photo.delay(990 + i)
