from contextlib import contextmanager
from time import time, sleep


class Lock(object):
    def __init__(self):
        self.lock = False


@contextmanager
def locker(some_lock):
    some_lock.lock = True
    yield some_lock


class TimeIt:

    def __enter__(self):
        self.started = time()
        return self

    def __exit__(self, *args):
        self.ended = time()
        self.result = self.ended - self.started

with TimeIt() as t:
    sleep(3)

print('Execution time was:', t.result)
