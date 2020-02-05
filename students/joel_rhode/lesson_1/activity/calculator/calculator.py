"""This module provides a basic math calculator."""


from .exceptions import InsufficientOperands


class Calculator(object):
    """Creates a basic math calculator."""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Inserts a number into the stack for later calculation."""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """Performs the math calculation specified by the operator."""
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Returns the addition sum of two numbers in the stack."""
        return self._do_calc(self.adder)

    def subtract(self):
        """Returns the subtraction difference of two numbers in the stack."""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Returns the multiplication product of two numbers in the stack."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Returns the division quotient of two numbers in the stack."""
        return self._do_calc(self.divider)
