"""
This module provides a calculator for addition, subtraction, multiplication, and division
"""

from .exceptions import InsufficientOperands

class Calculator(object):
    """A class used to represent a Calculator object"""
    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """A method that adds a number to a list"""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """A method that carries out a general operation between two numbers"""
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """A method that returns the sum of two operands"""
        return self._do_calc(self.adder)

    def subtract(self):
        """A method that returns the difference of two operands"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """A method that returns the product of two operands"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """A method that returns the quotient of two operands"""
        return self._do_calc(self.divider)
        