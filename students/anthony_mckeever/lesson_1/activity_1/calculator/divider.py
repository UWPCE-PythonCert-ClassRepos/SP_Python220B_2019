# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 10/16/2019

"""
divider Module:
    Classes:
        Divider - Provides logic for dividing numbers.
"""


class Divider():
    """ A class for dividing operands. """

    @staticmethod
    def calc(operand_a, operand_b):
        """
        Return the first number (a) divided by the second number (b).

        :operand_a: The first number to divid from.
        :operand_b: The second number to divid with.
        """
        return operand_a / operand_b
