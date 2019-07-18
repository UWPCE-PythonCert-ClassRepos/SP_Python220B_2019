"""
The Calculator Module
"""

from .exceptions import InsufficientOperands


class Calculator():
    """ The Calculator Class """
    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """ Push a number on the stack """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """ Run the calculation """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """ Execute Addition """
        return self._do_calc(self.adder)

    def subtract(self):
        """ Execute Subtraction """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """ Execute Multiplication """
        return self._do_calc(self.multiplier)

    def divide(self):
        """ Execute Division """
        return self._do_calc(self.divider)
