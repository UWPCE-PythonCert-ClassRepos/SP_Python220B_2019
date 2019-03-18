"""
recursion for debuging
"""

import sys
import logging

logging.basicConfig(level=logging.DEBUG)

def my_fun(n):
    logging.debug(n)
    if n == 2:
        return True
    return my_fun(n / 2)


if __name__ == '__main__':
    n = 100
    print(my_fun(n))
