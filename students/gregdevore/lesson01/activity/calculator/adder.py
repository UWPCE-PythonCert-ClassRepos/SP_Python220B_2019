"""
This module provides an addition operator
"""


class Adder(object):
    """
    Class for adding two numbers

    Methods:

        calc(operand_1, operand_2):
            Static method, takes two operands as input and returns their sum

    """
    @staticmethod
    def calc(operand_1, operand_2):
        """
        Method to add two numbers

        Args:

            operand_1, operand_2 (numeric):
                Numbers to add

        Returns the sum of the two operands

        """
        return operand_1 + operand_2
