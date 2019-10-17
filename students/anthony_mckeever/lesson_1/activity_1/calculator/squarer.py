# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 10/16/2019

"""
squarer Module:
    Classes:
        Squarer - Provides logic for squaring a number.
"""


class Squarer():
    """ A class for calculating the square of an operand. """

    @staticmethod
    def calc(operand):
        """
        Return the square of the operand.

        :operand:   The number to square.
        """
        return operand ** 2
