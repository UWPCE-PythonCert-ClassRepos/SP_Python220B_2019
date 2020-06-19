""" This module provides an addition operator. """


class Adder():
    '''Adder class, @staticmethod for adding two numbers'''

    @staticmethod
    def calc(operand_1, operand_2):
        '''Takes two operands, works left to right'''
        return operand_1 + operand_2
