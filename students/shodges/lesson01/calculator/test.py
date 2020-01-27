from unittest import TestCase

from adder import Adder
from subtracter import Subtracter
from multiplier import Multiplier
from divider import Divider
from calculator import Calculator

class AdderTests(TestCase):
    def test_adding(self):
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))

class SubtracterTests(TestCase):
    def test_subtracting(self):
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))

class MultiplierTest(TestCase):
    def test_multiplying(self):
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))

class DividerTest(TestCase):
    def test_dividing(self):
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i / j, divider.calc(i, j))
