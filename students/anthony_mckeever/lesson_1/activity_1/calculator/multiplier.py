# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# RedMine Issue - SchoolOps-10
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 10/16/2019

"""
multiplier Module:
    Classes:
        Multiplier - Provides logic for multiplying numbers.
"""


class Multiplier():
    """ A class for multiplying operands. """

    @staticmethod
    def calc(operand_a, operand_b):
        """
        Return the first number (operand_a) multiplied by the second
        number (operand_b).

        :operand_a: The first number to multiply from.
        :operand_b: The second number to multiply with.
        """
        return operand_a * operand_b
