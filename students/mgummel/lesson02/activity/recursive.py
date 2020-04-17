
"""
recursion for debuging
"""

import sys


def my_fun(i):
    if i == 2:
        return True
    return my_fun(i / 2)


if __name__ == '__main__':
    i = int(sys.argv[1])
    print(my_fun(i))

