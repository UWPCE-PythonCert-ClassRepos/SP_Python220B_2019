"""
This module provides a division operator
"""


class Divider(object):
    """
    Class for dividing two numbers

    Methods:

        calc(operand_1, operand_2):
            Static method, takes two operands as input and returns the quotient
            Quotient is calculated as operand_1 / operand_2

    """
    @staticmethod
    def calc(operand_1, operand_2):
        """
        Method to divide two numbers

        Args:

            operand_1, operand_2 (numeric):
                Numbers to divide

        Returns the quotient of the two operands (operand_1 / operand_2)

        """
        return operand_1/operand_2
