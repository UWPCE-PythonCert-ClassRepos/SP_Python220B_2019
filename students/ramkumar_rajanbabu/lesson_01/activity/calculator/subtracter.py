"""This module provides a subtraction operator."""

class Subtracter(object):
    """A class for subtracting operands."""
    
    @staticmethod
    def calc(operand_1, operand_2):
        """Subtracts the numbers.
        Args:
            operand_1: first number to subtract
            operand_2: second number to subtract
        Returns:
            the operand_2 from operand_1
        """
        return operand_1 - operand_2
