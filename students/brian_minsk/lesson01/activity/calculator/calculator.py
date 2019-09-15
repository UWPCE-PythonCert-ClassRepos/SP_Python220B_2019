""" calculator module

Classes:
    Calculator
"""

from .exceptions import InsufficientOperands

class Calculator():
    """ Class for arithmetical operations. """

    def __init__(self, adder, subtracter, multiplier, divider):
        """ Initialize a Calculator object. """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """ Insert a number for later calculation. """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """ Call the appropriate operator, replace the stack with the result,
        and return the result."""
        try:
            # Change the order of the calc operands. This corrects subtract
            # and divide without affecting add and multiply.
            # OLD result = operator.calc(self.stack[0], self.stack[1])
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """ Call _do_calc with the adder attribute and return the result. """
        return self._do_calc(self.adder)

    def subtract(self):
        """ Call _do_calc with the subtract attribute and return the result. """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """ Call _do_calc with the multiply attribute and return the result. """
        return self._do_calc(self.multiplier)

    def divide(self):
        """ Call _do_calc with the divide attribute and return the result. """
        # Handle ZeroDivisionError exception.
        try:
            result = self._do_calc(self.divider)
        except ZeroDivisionError:
            raise ZeroDivisionError
        else:
            return result
