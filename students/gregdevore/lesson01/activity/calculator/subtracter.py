"""
This module provides a subtraction operator
"""


class Subtracter(object):
    """
    Class for subtracting two numbers

    Methods:

        calc(operand_1, operand_2):
            Static method, takes two operands as input and returns the
            difference. Difference is calculated as operand_1 - operand_2

    """
    @staticmethod
    def calc(operand_1, operand_2):
        """
        Method to subtract two numbers

        Args:

            operand_1, operand_2 (numeric):
                Numbers to subtract

        Returns the difference of the two operands (operand_1 - operand_2)

        """
        return operand_1 - operand_2
