""" This module provides a calculator. """
from .exceptions import InsufficientOperands


class Calculator():
    ''' Takes in objects fromAdder(), Subtracter(), Multiplier(),
     and Divider(),call Calculator() for any of these purposes'''

    def __init__(self, adder, subtracter, multiplier, divider):
        ''' Initaters each operation from imported file,
        creates an empty list to put operands in'''
        self.adder = adder
        self.subtracter = subtracter
        self.multiplier = multiplier
        self.divider = divider

        self.stack = []

    def enter_number(self, number):
        '''Adds a number to the end of the stack'''
        self.stack.append(number)

    def _do_calc(self, operator):
        '''Runs the stack left to right -
        ensures that correct amount of elements in the list'''
        try:
            result = operator.calc(self.stack[0], self.stack[1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result

    def add(self):
        ''' Add operand1 to operand2'''
        return self._do_calc(self.adder)

    def subtract(self):
        ''' Subtract operand2 from operand1'''
        return self._do_calc(self.subtracter)

    def multiply(self):
        '''Multiply operand1 to operand2'''
        return self._do_calc(self.multiplier)

    def divide(self):
        '''Divide operand1 by operand2'''
        return self._do_calc(self.divider)
