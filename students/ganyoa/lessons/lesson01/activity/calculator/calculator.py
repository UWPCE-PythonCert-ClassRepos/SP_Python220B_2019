"""
This module provides a calculator.
"""


from .exceptions import InsufficientOperands


class Calculator():
    '''
    stores numbers entered by user for calculations
    '''

    def __init__(self, adder, subtracter, multiplier, divider):
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        '''submits number to list for later calculations'''
        self.stack.insert(0, number)
        # self.stack.append(0, number)

    def _do_calc(self, operator):
        '''confirms two operands are available for calculation'''
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        '''calls adder class with operands'''
        return self._do_calc(self.adder)

    def subtract(self):
        '''calls subtracter class with operands'''
        return self._do_calc(self.subtracter)

    def multiply(self):
        '''calls multiplier class with operands'''
        return self._do_calc(self.multiplier)

    def divide(self):
        '''calls divider class with operands'''
        return self._do_calc(self.divider)
