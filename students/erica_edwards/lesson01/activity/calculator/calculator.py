"""
This module implements a calculator operations
"""

from .exceptions import InsufficientOperands


class Calculator():
    """
    Implement calculator operations
    """

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        add number to stack

        Args:
            number (int): number
        """
        self.stack.insert(0, number)

    def _do_calc(self, operator):
        """
        Do calcualtion for specified operator

        Args:
            operator (object): object the implements the operator

        Raises:
            InsufficientOperands: Operand missing, or of incorrect type

        Returns:
            number: result of the calculation
        """
        try:
            result = operator.calc(self.stack[1], self.stack[0])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Perform addition

        Returns:
            number: result of addition
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Perform subtraction

        Returns:
            number: result of subtraction
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Perform multiplication

        Returns:
            number: result of multiplication
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Perform division

        Returns:
            number: result of division
        """
        return self._do_calc(self.divider)
