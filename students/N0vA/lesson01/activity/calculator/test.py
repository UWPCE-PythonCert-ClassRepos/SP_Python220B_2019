from unittest import TestCase
from unittest.mock import MagicMock

from adder import Adder
from subtracter import Subtracter
from multiplier import Multiplier
from divider import Divider
from calculator import Calculator
from exceptions import InsufficientOperands

class AdderTest(TestCase):

    def test_adding(self):
        adder = Adder()

        for x in range(-5, 10):
            for y in range(-5, 10):
                self.assertEqual(x + y, adder.calc(x, y))

class SubtracterTest(TestCase):

    def test_subtracting(self):

        subtracter = Subtracter()

        for x in range(-5, 10):
            for y in range(-5, 10):
                self.assertEqual(x - y, subtracter.calc(x, y))

class MultiplierTest(TestCase):

    def test_multiplying(self):

        multiplier = Multiplier()

        for x in range(-5, 10):
            for y in range(-5, 10):
                self.assertEqual(x * y, multiplier.calc(x, y))

class DividerTest(TestCase):

    def test_dividing(self):

        divider = Divider()

        for x in range(5, 10):
            for y in range(5, 10):
                self.assertEqual(x / y, divider.calc(x, y))

class CalculatorTest(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add
            
    def test_adder_call(self):
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)
