# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 10/16/2019

"""
Module Unit Tests

Tested Modules:
    Calculator
        Calculator
        Adder
        Subtacter
        Multiplier
        Divider
        Squarer
        Exceptions
"""

from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.squarer import Squarer
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class AdderTests(TestCase):
    """ A collection of Adder test cases """

    def test_adder(self):
        """
        Tests the Adder's calc method

        Expected Result Example: 2 + 2 = 4
        """
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    """ A collection of Subtracter test cases """

    def test_subtracter(self):
        """
        Tests the Subtracter's calc method

        Expected Result Example: 4 - 2 = 2
        """
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    """ A collection of Multiplier test cases """

    def test_multiplier(self):
        """
        Tests the Multiplier's calc method

        Expected Result Example: 3 * 2 = 6
        """
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    """ A collection of Divder test cases """

    def test_divider(self):
        """
        Tests the Divder's calc method

        Expected Result Example: 10 / 2 = 5
        """
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                if i != 0 and j != 0:
                    self.assertEqual(i / j, divider.calc(i, j))


class SquarerTests(TestCase):
    """ A collection of Squarer test cases """

    def test_adder(self):
        """
        Tests the Divder's calc method

        Expected Result Example: -2^2 = 4
        """
        squarer = Squarer()

        for i in range(-10, 10):
            self.assertEqual(i ** 2, squarer.calc(i))


class CalculatorTests(TestCase):
    """ A Calculator of Squarer test cases """

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()
        self.squarer = Squarer()

        self.calculator = Calculator(self.adder,
                                     self.subtracter,
                                     self.multiplier,
                                     self.divider,
                                     self.squarer)

    def test_insufficient_operands(self):
        """
        Tests all calculator operations throws InsufficientOperands exceptions
        if the inadequate amount of operands are provided.
        """
        with self.assertRaises(InsufficientOperands):
            self.calculator.square()

        self.calculator.enter_number(2)

        with self.assertRaises(InsufficientOperands):
            self.calculator.add()

        with self.assertRaises(InsufficientOperands):
            self.calculator.subtract()

        with self.assertRaises(InsufficientOperands):
            self.calculator.multiply()

        with self.assertRaises(InsufficientOperands):
            self.calculator.divide()

    def test_adder_call(self):
        """
        Tests that Add calls the adder's calc function
        """
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        """
        Tests that Subtract calls the subtracters's calc function
        """
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)

    def test_multiplier_call(self):
        """
        Tests that Multiply calls the multiplier's calc function
        """
        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(1, 2)

    def test_divider_call(self):
        """
        Tests that Divide calls the Divider's calc function
        """
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(1, 2)

    def test_squarer_call(self):
        """
        Tests that Square calls the Squarer's calc function
        """
        self.squarer.calc = MagicMock(return_value=0)

        self.calculator.enter_number(2)
        self.calculator.square()

        self.squarer.calc.assert_called_with(2)
