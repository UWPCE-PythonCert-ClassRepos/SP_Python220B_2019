# Advanced Programming In Python - Lesson 2 Activity 1: Automated Testing
# RedMine Issue - SchoolOps-12
# Code Poet: Anthony McKeever
# Start Date: 10/23/2019
# End Date: 10/23/2019

"""
recursion for debuging
"""

import sys


def my_fun(n):
    if n == 2:
        return True
    elif n < 1:
        return False

    return my_fun(n / 2)


if __name__ == '__main__':
    n = int(sys.argv[1])
    print(my_fun(n))
