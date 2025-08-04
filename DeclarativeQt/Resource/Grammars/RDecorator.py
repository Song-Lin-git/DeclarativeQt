import inspect
import os.path
from typing import Callable


def logPrivate(func: Callable):
    file_path = inspect.getfile(func)
    file_path = os.path.basename(file_path)
    line_number = inspect.getsourcelines(func)[1]
    log = "A private function called: " + f"{func.__name__} at file {file_path}: line {line_number}"
    print(log)
    return func


def private(func: Callable):
    return func
