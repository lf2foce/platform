import requests
import functools
import json

def slack_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        url = 'https://hooks.slack.com/services/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'
        headers = {'Content-type': 'application/json'}
        log = func(*args, **kwargs)
        print('zz')
        data = {"text": str(log)}
        data = json.dumps(data)
        response = requests.post(url, headers=headers, data=data)
    return wrapper

@slack_log
def noti(log):
    return log

noti = slack_log(noti)


# boiler code
import functools

def my_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        # return func(*args, **kwargs)  
        return value
    return wrapper

def say_whee(name):
    # do sth else
    return f"Hi {name}"


say_whee = my_decorator(say_whee)
say_whee('AB')