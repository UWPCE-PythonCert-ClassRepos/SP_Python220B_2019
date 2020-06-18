"""This module provides a calculator."""


from .exceptions import InsufficientOperands


class Calculator():
    """Class for calculating values"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Method for adding a number to the calculator stack"""
        self.stack.append(number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Method to return the adder value"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Method to return the subtracter value"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Method to return the multiplier value"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Method to return the divider value"""
        return self._do_calc(self.divider)
