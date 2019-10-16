# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 
# 
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10

"""
multiplier Module:
    Classes:
        Multiplier - Provides logic for multiplying numbers.
"""


class Multiplier(object):
    """ A class for multiplying operands. """


    @staticmethod
    def calc(a, b):
        """
        Return the first number (a) multiplied by the second number (b).

        :a: The first number to multiply from.
        :b: The second number to multiply with.
        """
        return a * b