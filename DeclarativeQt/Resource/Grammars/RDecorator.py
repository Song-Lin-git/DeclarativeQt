import inspect
import os.path
from typing import Callable

import colorama
from colorama import Fore

colorama.init(autoreset=True)


def logPrivate(func: Callable):
    file = os.path.basename(inspect.getfile(func))
    line = inspect.getsourcelines(func)[1]
    func = f"{func.__name__}"
    print(f"{Fore.YELLOW}Private: {func} at {file}: line-{line}")
    return func


def private(func: Callable):
    return func
