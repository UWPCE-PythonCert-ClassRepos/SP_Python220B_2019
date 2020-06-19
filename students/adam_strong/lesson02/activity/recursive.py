#!/usr/bin/env python
"""
recursion for debuging:

>>>Problem with script from debugging:
If argv is not x >= 2 where x is a multiple of two the script will recur, this is because
the return my_fun(i/2) will never reach the i == 2 conditional and end by returning true.

Changed the behavior: If the value is greater than two and has a mod of 0 it can recur
If not, it will return false

"""

import sys


def my_fun(i):
    if i == 2:
        return True
    elif (i > 2) and (i%2 == 0): #Added to check if the value will ever actually hit 2 in recurssion
        return my_fun(i / 2)
    else:
        return False

    #return my_fun(i / 2)

if __name__ == '__main__':
    i = int(sys.argv[1])
    print(my_fun(i))

