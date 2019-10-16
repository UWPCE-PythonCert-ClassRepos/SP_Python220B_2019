# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 
# 
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10

"""
adder Module:
    Classes:
        Adder - Provides logic for adding numbers together.
"""


class Adder(object):
    """ A class for adding operands together. """


    @staticmethod
    def calc(a, b):
        """
        Return two numbers added together.

        :a: The first number to add.
        :b: The second number to add.
        """
        return a + b