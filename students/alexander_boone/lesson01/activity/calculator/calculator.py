"""
This module contains the calculator class and associated methods.
"""

from .exceptions import InsufficientOperands


class Calculator:
    """
    This is a class for calculator.

    It contains methods to perform four operations:

    - Addition
    - Subtraction
    - Multiplication
    - Division
    """
    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Enter number into the calculator stack at position 0."""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Perform calculation designated by operator on current stack.
        """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Perform addition operation."""
        return self._do_calc(self.adder)

    def subtract(self):
        """Perform division operation."""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Perform multiplication operation."""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Perform division operation."""
        return self._do_calc(self.divider)
