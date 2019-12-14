"""calculator module"""

from .exceptions import InsufficientOperands


class Calculator():
    """contains methods to store input values and call calculations"""

    def __init__(self, adder, subtracter, multiplier, divider):
        """class initilzation"""
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """populates list (stack) with user input values"""
        self.stack.insert(1, number)

    def _do_calc(self, operator):
        """private method
        checks operands and returns calculated value to the stack"""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """calls module initiated to perform calculation"""
        return self._do_calc(self.adder)

    def subtract(self):
        """calls module initiated to perform calculation"""
        return self._do_calc(self.subtracter)

    def multiply(self):
        """calls module initiated to perform calculation"""
        return self._do_calc(self.multiplier)

    def divide(self):
        """calls module initiated to perform calculation"""
        return self._do_calc(self.divider)
