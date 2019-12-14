"""
This module provides a division operator
"""
from .exceptions import DivideByZero


class Divider():
    """divides first operand by second, returns result"""

    @staticmethod
    def calc(operand_1, operand_2):
        """performs calculation"""
        try:
            return operand_1/operand_2
        except ZeroDivisionError:
            raise DivideByZero
