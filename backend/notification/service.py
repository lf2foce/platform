import requests
import json
from backend.proj.celery import app as celery_app
from backend.utils.decorator import slack_noti


@celery_app.task(name="send_slack_message")
@slack_noti
def send_slack_message(message=None):
    message = "from decorator"
    return message


# url = ''

# headers = {'Content-type': 'application/json'}

# @celery_app.task(name='send_slack_message1')
# def send_slack_message1(url=url, message=None):
#     data = {"text": message}
#     data = json.dumps(data)
#     response = requests.post(url, headers=headers, data=data)
#     return response
