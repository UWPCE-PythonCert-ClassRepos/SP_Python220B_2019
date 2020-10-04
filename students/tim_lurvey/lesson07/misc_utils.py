""" Documentation for misc_utils
A collection of various useful function to be reused outside class"""

import time
import logging

logger = logging.getLogger('__main__')

_func_count = {}


def func_timer(func):
    """time a function, record how many times called"""
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time() - start
        _func_count.update({func.__name__:
                            _func_count.get(func.__name__, 0) + 1})
        logger.info(f"TIMER: {func.__name__}() -> {end:10.7f} sec | "
                    f"COUNT: {_func_count.get(func.__name__)}")
        return result
    return inner
