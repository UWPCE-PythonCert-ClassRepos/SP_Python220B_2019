"""
recursion for debuging
"""

import sys
import logging

log_format = "%(asctime)s %(filename)s:%(lineno)-4d %(levelname)s %(message)s"
logging.basicConfig(level=logging.WARNING, format=log_format, filename='recursive.log')

def my_fun(n):
    logging.debug(n)
    if n == 2:
        return True
    try:
        return my_fun(n/2)
    except RecursionError:
        logging.warning("This number will never go to 2")


if __name__ == '__main__':
    n = int(sys.argv[1])
    print(my_fun(n))
