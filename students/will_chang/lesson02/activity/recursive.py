#!/usr/bin/env python

"""
recursion for debuging
"""

"""
This function runs into an infinite recursion issue when the
number n is odd. An odd number will keep dividing itself by 2,
converging towards 0. An even number will simply return True as
the number n will eventually divide itself into a value of 2.

Adding the conditional: 'if n < 1: return False' allows the program
to terminate and return False for odd numbers.
"""
import sys


def my_fun(n):
    if n < 1:
        return False
    if n == 2:
        return True
    return my_fun(n / 2)


if __name__ == '__main__':
    n = int(sys.argv[1])
    print(my_fun(n))