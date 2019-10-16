# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 
# 
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10

"""
squarer Module:
    Classes:
        Squarer - Provides logic for squaring a number.
"""


class Squarer(object):
    """ A class for calculating the square of an operand. """


    @staticmethod
    def calc(operand):
        """
        Return the square of the operand.

        :operand:   The number to square.
        """
        return operand ** 2