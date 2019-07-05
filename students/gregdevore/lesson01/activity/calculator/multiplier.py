"""
This module provides a multiplication operator
"""


class Multiplier(object):
    """
    Class for multiplying two numbers

    Methods:

        calc(operand_1, operand_2):
            Static method, takes two operands as input and returns their
            product

    """
    @staticmethod
    def calc(operand_1, operand_2):
        """
        Method to multiply two numbers

        Args:

            operand_1, operand_2 (numeric):
                Numbers to multiply

        Returns the product of the two operands

        """
        return operand_1*operand_2
