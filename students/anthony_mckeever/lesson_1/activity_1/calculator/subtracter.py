# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 
# 
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10

"""
subtracter Module:
    Classes:
        Subtacter - Provides logic for subtracting numbers.
"""


class Subtracter(object):
    """ A class for subtracting operands. """


    @staticmethod
    def calc(a, b):
        """
        Return the second number (b) from the first number (a).

        :a: The first number to subtract.
        :b: The second number to subtract.
        """
        return a - b