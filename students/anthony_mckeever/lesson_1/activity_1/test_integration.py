# Advanced Programming In Python - Lesson 1 Activity 1: Automated Testing
# RedMine Issue - SchoolOps-10
# Code Poet: Anthony McKeever
# Start Date: 10/15/2019
# End Date: 10/16/2019

"""
Module Integration Tests

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

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.squarer import Squarer
from calculator.calculator import Calculator


class ModuleTests(TestCase):
    """ A collection of module integration tests """

    def test_module(self):
        """
        Tests all calculator modules work together nicely and the correct
        module is called for the given calculation operation.
        """
        calculator = Calculator(Adder(),
                                Subtracter(),
                                Multiplier(),
                                Divider(),
                                Squarer())

        calculator.enter_number(2)
        calculator.square()  # result = 4

        calculator.enter_number(3)
        calculator.multiply()  # result = 12

        calculator.enter_number(8)
        calculator.add()  # result = 20

        calculator.enter_number(4)
        calculator.divide()  # result = 5

        calculator.enter_number(6)
        result = calculator.subtract()  # result = -1

        self.assertEqual(-1, result)
