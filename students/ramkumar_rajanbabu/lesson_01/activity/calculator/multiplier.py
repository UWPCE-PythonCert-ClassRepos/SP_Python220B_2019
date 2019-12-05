"""This module provides a multiplication operator."""

class Multiplier(object):
    """A class for multipyling operands."""

    @staticmethod
    def calc(operand_1, operand_2):
        """Multiplies the numbers.
        Args:
            operand_1: first number to multiply
            operand_2: second number to multiply
        Returns:
            both numbers multiplied together
        """
        return operand_1 * operand_2
