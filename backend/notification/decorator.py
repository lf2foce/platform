import requests
import functools
import json
import logging

log = logging.getLogger(__name__)

# TODO: send slack message when task fail
def slack_noti(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        url = 'https://hooks.slack.com/services/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'
        headers = {'Content-type': 'application/json'}
        try:
            message = func(*args, **kwargs)
            data = {"text": str(message)}
            data = json.dumps(data)
            response = requests.post(url, headers=headers, data=data)
            return message
        except Exception as e:
            log.warning(
                f"Notification not sent. No plugin is active."
            )    
    return wrapper

# @slack_noti
# def noti(message):
#     return message

# # equivalent
# noti = slack_noti(noti)

# noti('run noti from decorator')

# ==== snippet code =====
# import functools

# def my_decorator(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         # Do something before
#         value = func(*args, **kwargs)
#         # Do something after
#         # return func(*args, **kwargs)  
#         return value
#     return wrapper

# def say_whee(name):
#     # do sth else
#     return f"Hi {name}"


# say_whee = my_decorator(say_whee)
# say_whee('AB')