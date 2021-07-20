import requests
import json


url = 'https://hooks.slack.com/services/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'

headers = {'Content-type': 'application/json'}

def send_slack_message(url=url, message=None):
    data = {"text": message}
    data = json.dumps(data)
    response = requests.post(url, headers=headers, data=data)
    return response
