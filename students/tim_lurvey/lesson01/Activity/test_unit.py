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
