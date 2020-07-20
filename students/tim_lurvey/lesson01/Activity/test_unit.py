#!/usr/bin/env python
import sys
import unittest

sys.path.append(r"C:\\Users\\pants\\PycharmProjects\\SP_Python220B_2019\\")
# from lessons.lesson01.activity.calculator import calculator
from lessons.lesson01.activity.calculator.adder import Adder
from lessons.lesson01.activity.calculator.subtracter import Subtracter
from lessons.lesson01.activity.calculator.multiplier import Multiplier
from lessons.lesson01.activity.calculator.divider import Divider
from Activity.calc.calc_fix import Calculator


# class BaseTest(unittest.TestCase):
#     C = Calculator(adder=Adder,
#                    subtracter=Subtracter,
#                    multiplier=Multiplier,
#                    divider=Divider)
#
#     def __init__(self, symbol: str, operand: object):
#         """inherit from parent class
#         :type symbol: string ('+' '/' '*' etc...)
#         :type operand: class method (__builtins__.__add__, etc)
#         """
#         super().__init__()
#         # set new variables for dynamic function
#         self.SYM = symbol
#         self.OP = operand
#
#     def t(self, p_n):
#         for i in range(1, p_n * 9, p_n * 1):
#             for j in range(1, p_n * 10, p_n * 1):
#                 self.C.enter_number(i)
#                 self.C.enter_number(j)
#                 self.assertEqual(first=self.OP(i, j),
#                                  second=self.C.add(),
#                                  msg="{i} {s} {j}".format(i=i,
#                                                           s=self.SYM,
#                                                           j=j))
#
#
# class AdderTests(BaseTest):
#
#     def __init__(self):
#         super().__init__(symbol='+', operand=operator.add())
#
#     def test_positives(self):
#         self.t(p_n=1)
#
#     def test_negatives(self):
#         self.t(p_n=-1)


class AdderTests(unittest.TestCase):
    c = Calculator(adder=Adder,
                   subtracter=Subtracter,
                   multiplier=Multiplier,
                   divider=Divider)

    def test_positives(self):
        for i in range(1, 9):
            for j in range(1, 10):
                self.c.enter_number(i)
                self.c.enter_number(j)
                self.assertEqual((i + j), self.c.add(), "{i} + {j}".format(i=i, j=j))

    def test_negatives(self):
        for i in range(0, -9, -1):
            for j in range(0, -10, -1):
                self.c.enter_number(i)
                self.c.enter_number(j)
                self.assertEqual((i + j), self.c.add(), "{i} + {j}".format(i=i, j=j))


class SubtractorTests(unittest.TestCase):
    c = Calculator(adder=Adder,
                   subtracter=Subtracter,
                   multiplier=Multiplier,
                   divider=Divider)

    def test_positives(self):
        for i in range(1, 9):
            for j in range(1, 10):
                self.c.enter_number(i)
                self.c.enter_number(j)
                self.assertEqual((i - j), self.c.subtract(), "{i} - {j}".format(i=i, j=j))

    def test_negatives(self):
        for i in range(0, -9, -1):
            for j in range(0, -10, -1):
                self.c.enter_number(i)
                self.c.enter_number(j)
                self.assertEqual((i - j), self.c.subtract(), "{i} - {j}".format(i=i, j=j))


class MultiplierTests(unittest.TestCase):
    c = Calculator(adder=Adder,
                   subtracter=Subtracter,
                   multiplier=Multiplier,
                   divider=Divider)

    def test_positives(self):
        for i in range(1, 9):
            for j in range(1, 10):
                self.c.enter_number(i)
                self.c.enter_number(j)
                self.assertEqual((i * j), self.c.multiply(), "{i} * {j}".format(i=i, j=j))

    def test_negatives(self):
        for i in range(0, -9, -1):
            for j in range(0, -10, -1):
                self.c.enter_number(i)
                self.c.enter_number(j)
                self.assertEqual((i * j), self.c.multiply(), "{i} * {j}".format(i=i, j=j))


class DividerTests(unittest.TestCase):
    c = Calculator(adder=Adder,
                   subtracter=Subtracter,
                   multiplier=Multiplier,
                   divider=Divider)

    def test_positives(self):
        for i in range(1, 9):
            for j in range(1, 10):
                self.c.enter_number(i)
                self.c.enter_number(j)
                self.assertEqual((i / j), self.c.divide(), "{i} / {j}".format(i=i, j=j))

    def test_negatives(self):
        for i in range(-1, -9, -1):
            for j in range(-1, -10, -1):
                self.c.enter_number(i)
                self.c.enter_number(j)
                self.assertEqual((i / j), self.c.divide(), "{i} / {j}".format(i=i, j=j))
