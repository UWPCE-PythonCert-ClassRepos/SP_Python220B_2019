# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 
# 
# Studio Starchelle RedMine - SchoolOps: http://redmine/issues/10

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
    
    def test_adder(self):
        adder = Adder()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))


class SubtracterTests(TestCase):
    
    def test_subtracter(self):
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))


class MultiplierTests(TestCase):
    
    def test_multiplier(self):
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))


class DividerTests(TestCase):
    
    def test_divider(self):
        divider = Divider()

        for i in range(-10, 10):
            for j in range(-10, 10):
                if i != 0 and j != 0:
                    self.assertEqual(i / j, divider.calc(i, j))


class SquarerTests(TestCase):
    
    def test_adder(self):
        squarer = Squarer()

        for i in range(-10, 10):
            self.assertEqual(i ** 2, squarer.calc(i))


class CalculatorTests(TestCase):

    def setUp(self):
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()
        self.squarer = Squarer()

        self.calculator = Calculator(self.adder, self.subtracter,self.multiplier, self.divider, self.squarer)


    def test_insufficient_operands(self):
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


    def test_squarer_call(self):
        self.squarer.calc = MagicMock(return_value=0)

        self.calculator.enter_number(2)
        self.calculator.square()

        self.squarer.calc.assert_called_with( 2)


class ModuleTests(TestCase):

    def test_module(self):
        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider(), Squarer())

        calculator.enter_number(2)
        calculator.square() # result = 4

        calculator.enter_number(3)
        calculator.multiply() # result = 12

        calculator.enter_number(8)
        calculator.add() # result = 20

        calculator.enter_number(4)
        calculator.divide() # result = 5

        calculator.enter_number(6)
        result = calculator.subtract() # result = -1

        self.assertEqual(-1, result)
