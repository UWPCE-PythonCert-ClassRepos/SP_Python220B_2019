"""Module Integration Tests"""

from unittest import TestCase

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator

class ModuleTests(TestCase):
    """Tests module integration"""
    
    def test_module(self):
        """Tests all calculator modules."""
    
        calculator = Calculator(Adder(), 
                                Subtracter(), 
                                Multiplier(), 
                                Divider())

        calculator.enter_number(5)
        calculator.enter_number(2)

        calculator.multiply() #10

        calculator.enter_number(46)

        calculator.add() #56

        calculator.enter_number(8)

        calculator.divide() #7

        calculator.enter_number(1)

        result = calculator.subtract() #6

        self.assertEqual(6, result) #Result should equal 6
