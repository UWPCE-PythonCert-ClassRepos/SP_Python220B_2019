"""This module provides a subtraction operator"""


class Subtracter():
    '''Subtracter class, @staticmethod for subtracting two numbers'''

    @staticmethod
    def calc(operand_1, operand_2):
        '''Takes two operands, works left to right'''
        return operand_1 - operand_2
