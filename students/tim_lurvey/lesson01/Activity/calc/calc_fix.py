#!/usr/bin/env python

from lessons.lesson01.activity.calculator import calculator
from lessons.lesson01.activity.calculator.calculator import InsufficientOperands


class Calculator(calculator.Calculator):
    """Monkey patch the original class method with error"""
    def __init__(self, adder, subtracter, multiplier, divider):
        super().__init__(adder, subtracter, multiplier, divider)

    def enter_number(self, number):
        """Monkey patch the original class method with error"""
        self.stack.append(number)

    def _do_calc(self, operator):
        try:
            result = operator.calc(self.stack[-2], self.stack[-1])
        except IndexError:
            raise InsufficientOperands

        self.stack = [result]
        return result
