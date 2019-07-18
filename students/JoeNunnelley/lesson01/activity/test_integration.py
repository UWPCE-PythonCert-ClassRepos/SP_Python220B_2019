from unittest import TestCase
from unittest.mock import MagicMock

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands


class ModuleTests(TestCase):

    def test_module(self):

        calculator = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calculator.enter_number(5)
        calculator.enter_number(2)

        result = calculator.multiply()
        self.assertEqual(10, result)

        calculator.enter_number(46)
        result = calculator.add()
        self.assertEqual(56, result)

        calculator.enter_number(8)
        result = calculator.divide()
        self.assertEqual(8 / 56, result)

        calculator.enter_number(1)
        result = calculator.subtract()
        self.assertEqual(1 - (8 / 56), result)
