
import time
import os
from .celery import app



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


# dynamically task #chưa dùng
PLUGIN_FOLDER = os.path.join(os.path.dirname(__file__), 'tasks')
def _absolutepath(filename):
    """ Return the absolute path to the filename"""
    return os.path.join(PLUGIN_FOLDER, filename)
    
@app.task
def tasks(funcname, *args, **kwargs):
    try:
        funcname = funcname.replace('-', '_')
        funcname += '.py'
        func = _absolutepath(funcname)
        ns = {}
        with open(func) as f:
            code = compile(f.read(), func, 'exec')
            eval(code, ns, ns)
        return ns['task'](*args, **kwargs)
    except IOError as e:
       # Manage IOError
       raise e