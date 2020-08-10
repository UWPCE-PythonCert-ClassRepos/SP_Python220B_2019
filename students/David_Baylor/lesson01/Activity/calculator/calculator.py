""" This module provides a calculator. """


from calculator.exceptions import InsufficientOperands


class Calculator():
    """
    Calculator does not do any calulations its self but redirects to
    other classes.
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """added a number to the stack."""
        self.stack.append(number)

    def _do_calc(self, operator):
        """calls a class based on the opporation and passes it the stack."""
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        "used by _do_calc() to call the addition class"
        return self._do_calc(self.adder)

    def subtract(self):
        "used by _do_calc() to call the subtraction class"
        return self._do_calc(self.subtracter)

    def multiply(self):
        "used by _do_calc() to call the multiplication class"
        return self._do_calc(self.multiplier)

    def divide(self):
        "used by _do_calc() to call the division class"
        return self._do_calc(self.divider)
