""" This module provides a multiplication operator. """


class Multiplier():
    '''Multiplier class, @staticmethod for multiplying two numbers'''

    @staticmethod
    def calc(operand_1, operand_2):
        '''Takes two operands, works left to right'''
        return operand_1 * operand_2
