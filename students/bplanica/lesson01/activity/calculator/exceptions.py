"""
This module contains an exception when
there are any number of operands other than two
"""


class InsufficientOperands(Exception):
    """When an exception is raised, print message to the user"""
    print("There are insufficient operands")


class DivideByZero(Exception):
    """When an exception is raised, print message to the user"""
    print("You cannot divide by zero")
