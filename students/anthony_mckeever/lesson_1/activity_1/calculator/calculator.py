# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# RedMine Issue - SchoolOps-10
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 10/16/2019

"""
calculator Module:
    Classes:
        Calculator - A module for calculating numbers.
"""

from .exceptions import InsufficientOperands


class Calculator():
    """
    A class that calculates numbers using a desired operation

    Usage:
        calculator = Calculator(adder, subtacter, multiplier, divider, squarer)
        calculator.enter_number(1)
        calculator.enter_number(3)
        result = calculator.add() # Return value = 4
    """

    def __init__(self, adder, subtracter, multiplier, divider, squarer):
        """
        Initializes the Calculator Class

        :self:          The Class
        :adder:         The Addition operation class
        :subtracer:     The Subtraction operation class
        :multiplier:    The Multiplication operation class
        :divider:       The Division operation class
        :squarer:       The Square operation class
        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider
        self.squarer = squarer

        self.stack = []

    def enter_number(self, number):
        """
        Insert a number into the calculator's stack at position stack[0]

        :self:      The Class
        :number:    The number to insert.
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Performs the desired calculation operation.

        :self:      The Class
        :operator:  The operation to perform.
        """
        try:
            if operator is self.squarer:
                result = operator.calc(self.stack[0])
            else:
                result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """ Return the result of the numbers in the stack added together. """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Return the result of the numbers in the stack subtracted from
        each other.
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Return the result of the numbers in the stack multiplied together.
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Return the result of the numbers in the stack divided from each other.
        """
        return self._do_calc(self.divider)

    def square(self):
        """ Return the result of squaring the number in the stack. """
        return self._do_calc(self.squarer)
