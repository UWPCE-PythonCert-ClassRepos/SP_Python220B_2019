# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 10/16/2019

"""
adder Module:
    Classes:
        Adder - Provides logic for adding numbers together.
"""


class Adder():
    """ A class for adding operands together. """

    @staticmethod
    def calc(operand_a, operand_b):
        """
        Return two numbers added together.

        :operand_a: The first number to add.
        :operand_b: The second number to add.
        """
        return operand_a + operand_b
