"""
This module provides a calculator object
"""

from .exceptions import InsufficientOperands


class Calculator(object):
    """
    Class for creating a calculator object

    Methods:

        enter_number(self, number):
            Adds number to stack of operands

        _do_calc(self, operator):
            Returns the result of calling operator function with operand stack

        add(self):
            Defines adder method

        subtract(self):
            Defines subtracter method

        multiply(self):
            Defines multiplier method

        divide(self):
            Defines divider method

    """
    def __init__(self, adder, subtracter, multiplier, divider):
        """
        Creates a calculator object

        Args:
            adder, subtracter, multiplier, divider (objects):
                Defines operators to power calculator

        """
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        """
        Adds number to current operand stack

        Args:
            number (numeric):
                Number to add to operand stack
        """
        # Changed insert to append. Append is constant time and ensures
        # unit tests pass with expected behavior
        self.stack.append(number)

    def _do_calc(self, operator):
        """
        Performs calculation defined in 'operator', stores result in operand
        stack

        Args:
            operator (object):
                Method that takes two operands as input and returns a value

        Returns:
            result (numeric):
                Result of computation performed by operator
        """
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        """
        Defines adder operator
        """
        return self._do_calc(self.adder)

    def subtract(self):
        """
        Defines subtracter operator
        """
        return self._do_calc(self.subtracter)

    def multiply(self):
        """
        Defines multiplier operator
        """
        return self._do_calc(self.multiplier)

    def divide(self):
        """
        Defines divider operator
        """
        return self._do_calc(self.divider)
