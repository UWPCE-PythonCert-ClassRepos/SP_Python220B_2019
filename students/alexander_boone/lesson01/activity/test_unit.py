"""
This module contains all unit tests for the calculator.
"""

from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class AdderTests(TestCase):
    """Contain tests for Adder class."""
    def test_adding(self):
        """Perform tests on Adder class."""
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(j, i))


class SubtracterTests(TestCase):
    """Contain tests for Subtracter class."""
    def test_subtracting(self):
        """Perform tests on Subtracter class."""
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i-j, subtracter.calc(j, i))


class MultiplierTests(TestCase):
    """Contain tests for Multiplier class."""
    def test_multiplying(self):
        """Perform tests on Multiplier class."""
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i*j, multiplier.calc(j, i))


class DividerTests(TestCase):
    """Contain tests for Divider class."""
    def test_dividing(self):
        """Perform tests on Divider class."""
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                if j != 0:
                    self.assertEqual(i/j, divider.calc(j, i))


class CalculatorTests(TestCase):
    """Contain tests for Calculator class."""
    def setUp(self):
        """Initialize calculator with new operator objects."""
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, self.subtracter,
                                     self.multiplier, self.divider)

    def test_insufficient_operands(self):
        """Test Insufficient Operands exception."""
        self.calculator.enter_number(0)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

    def test_adder_call(self):
        """Test a call to the Adder function using MagicMock."""
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(2, 1)

    def test_subtracter_call(self):
        """Test a call to the Divider function using MagicMock."""
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(2, 1)
