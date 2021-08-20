from collections import deque
from datetime import datetime
import functools

print("from test1.py")


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = datetime.now()
        func(*args, **kwargs)
        # return func(*args, **kwargs)
        end = datetime.now() - start
        print(end)
        return end

    return wrapper


@timeit
def l_():
    l_ = list()
    for i in range(40000):
        l_.insert(0, i)


@timeit
def d_():
    d = deque()
    for i in range(40000):
        d.appendleft(i)


d_()
