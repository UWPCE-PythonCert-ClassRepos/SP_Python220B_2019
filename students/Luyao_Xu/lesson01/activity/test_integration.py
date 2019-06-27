from .calculator import *
from unittest import TestCase
from unittest.mock import MagicMock


class ModuleTests(TestCase):

    def test_module(self):

        calc = Calculator(Adder(), Subtracter(), Multiplier(), Divider())

        calc.enter_number(5)
        calc.enter_number(2)

        calc.multiply()

        calc.enter_number(46)

        calc.add()

        calc.enter_number(8)

        calc.divide()

        calc.enter_number(1)

        result = calc.subtract()

        self.assertEqual(6, result)


