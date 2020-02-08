"""
Calculator - Provide logic to perform calculations on two operands
"""


from .exceptions import InsufficientOperands


class Calculator(object):
    """ A class for performing calculations"""

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """Enters two operands into array"""
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """Adds numbers together"""
        return self._do_calc(self.adder)

    def subtract(self):
        """Subtracts numbers together"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """Multiplies numbers together"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """Divides numbers together"""
        return self._do_calc(self.divider)
