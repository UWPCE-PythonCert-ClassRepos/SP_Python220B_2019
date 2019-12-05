"""This module provides a division operator."""

class Divider(object):
    """A class for dividing operands."""
    
    @staticmethod
    def calc(operand_1, operand_2):
        """Divides the numbers.
        Args:
            operand_1: first number to divide
            operand_2: second number to divide
        Returns:
            the operand_2 from operand_1
        """
        return operand_1 / operand_2
