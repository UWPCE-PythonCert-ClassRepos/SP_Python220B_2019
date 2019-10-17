# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 10/16/2019

"""
subtracter Module:
    Classes:
        Subtacter - Provides logic for subtracting numbers.
"""


class Subtracter():
    """ A class for subtracting operands. """

    @staticmethod
    def calc(operand_a, operand_b):
        """
        Return the second number (operand_b) from the first number (operand_a).

        :operand_a: The first number to subtract.
        :operand_b: The second number to subtract.
        """
        return operand_a - operand_b
