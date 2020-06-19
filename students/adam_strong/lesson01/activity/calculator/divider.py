""" This module provides a division operator."""


class Divider():
    '''Divider class, @staticmethod for dividing two numbers'''

    @staticmethod
    def calc(operand_1, operand_2):
        '''Takes two operands, works left to right'''
        return operand_1 / operand_2
