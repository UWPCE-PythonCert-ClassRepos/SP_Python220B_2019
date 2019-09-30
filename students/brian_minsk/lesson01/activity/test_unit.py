from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands

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


class MultiplierTests(TestCase):

    def test_multiplying(self):
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):

    def test_dividing(self):
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                try:
                    self.assertEqual(i / j, divider.calc(i, j))
                except ZeroDivisionError:
                    pass  # Not testing divide by zero here.
                          # See CalculatorTests.test_zero_division_error


class CalculatorTests(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter, self.multiplier, self.divider)

    def test_insufficient_operands(self):
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()
            self.calculator.subtract()
            self.calculator.multiply()
            self.calculator.divide()

    def test_zero_division_error(self):
        self.calculator.enter_number(1)
        self.calculator.enter_number(0)

        with self.assertRaises(ZeroDivisionError):
            self.calculator.divide()

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

    def test_multiplier_call(self):
        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(1, 2)

    def test_divider_call(self):
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(1, 2)

    def test_operation_sequence(self):
        self.adder.calc = MagicMock(return_value=0)
        self.subtracter.calc = MagicMock(return_value=0)
        self.multiplier.calc = MagicMock(return_value=0)
        self.divider.calc = MagicMock(return_value=0)

        operations = (self.calculator.add,
                      self.calculator.subtract,
                      self.calculator.multiply,
                      self.calculator.divide)

        for operation_1 in operations:
            for operation_2 in operations:
                self.calculator.enter_number(1)
                self.calculator.enter_number(2)
                operation_1()
                self.calculator.enter_number(3)
                operation_2()


