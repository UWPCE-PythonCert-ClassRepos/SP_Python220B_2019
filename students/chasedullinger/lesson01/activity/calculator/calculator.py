""" This module provides a calculator. """


from .exceptions import InsufficientOperands


class Calculator:
    """This is the main calculator class"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Function to add a number to the stack"""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError as insuffientops:
            raise InsufficientOperands from insuffientops

        self.stack = [result]
        return result

    def add(self):
        """Adds the numbers in the stack"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Subtracts the numbers in the stack"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Multiplies the numbers in the stack"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Divides the numbers in the stack"""
        return self._do_calc(self.divider)
