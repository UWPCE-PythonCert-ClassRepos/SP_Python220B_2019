"""This module creates a calculator."""

from .exceptions import InsufficientOperands


class Calculator:
    """Creating a calculator."""
    def __init__(self, adder, subtracter, multiplier, divider):
        """s"""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """s"""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """s"""
        try:
            # Old result = operator.calc(self.stack[0], self.stack[1])
            # The old affects subtract and divide by causing issues
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """s"""
        return self._do_calc(self.adder)

    def subtract(self):
        """3"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """s"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """s"""
        return self._do_calc(self.divider)
