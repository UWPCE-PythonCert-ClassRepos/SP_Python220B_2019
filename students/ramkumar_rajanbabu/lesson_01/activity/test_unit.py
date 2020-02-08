"""
Module Unit Tests
"""

from unittest import TestCase
from unittest.mock import MagicMock #python3
#from mock import MagicMock #python2

from calculator.adder import Adder
from calculator.subtracter import Subtracter
from calculator.multiplier import Multiplier
from calculator.divider import Divider
from calculator.calculator import Calculator
from calculator.exceptions import InsufficientOperands

class AdderTests(TestCase):
    """
    Tests for adder class
    """

    def test_adding(self): #Test method has to begin with word "test"
        """
        Tests adder calc method
        """
        
        adder = Adder() #Instantiate

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i + j, adder.calc(i, j))

class SubtracterTests(TestCase):
    """
    Tests for subtracter class
    """

    def test_subtracting(self): 
        """
        Tests subtracter calc method
        """
        
        subtracter = Subtracter()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i - j, subtracter.calc(i, j))
                
class MultiplierTests(TestCase): 
    """
    Tests for multiplier class
    """
    
    def test_multipling(self): 
        """
        Tests multiplier calc method
        """
        
        multiplier = Multiplier()

        for i in range(-10, 10):
            for j in range(-10, 10):
                self.assertEqual(i * j, multiplier.calc(i, j))
                
class DividerTests(TestCase): 
    """
    Tests for divider class
    """

    def test_dividing(self): 
        """
        Tests divider calc method
        """
        
        divider = Divider()

        try:
            for i in range(-10, 10):
                for j in range(-10, 10):
                    self.assertEqual(i / j, divider.calc(i, j))
        except ZeroDivisionError:
            pass #print("Cannot divide by zero.") Double check what to do here
                
class CalculatorTests(TestCase):
    """
    Tests for calculator class
    """

    def setUp(self): #Run before test method is run
        """
        Setup
        """
        
        self.adder = Adder()
        self.subtracter = Subtracter()
        self.multiplier = Multiplier()
        self.divider = Divider()

        self.calculator = Calculator(self.adder, 
                                     self.subtracter, 
                                     self.multiplier, 
                                     self.divider)

    def test_insufficient_operands(self):
        """
        Insufficient operands test
        """
        
        self.calculator.enter_number(0)

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
        Adder test
        """
        
        self.adder.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.add()

        self.adder.calc.assert_called_with(1, 2)

    def test_subtracter_call(self):
        """
        Subtracter test
        """
        
        self.subtracter.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.subtract()

        self.subtracter.calc.assert_called_with(1, 2)
        
    def test_multiplier_call(self):
        """
        Multiplier test
        """
        
        self.multiplier.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.multiply()

        self.multiplier.calc.assert_called_with(1, 2)
        
    def test_divider_call(self):
        """
        Divider test
        """
        
        self.divider.calc = MagicMock(return_value=0)

        self.calculator.enter_number(1)
        self.calculator.enter_number(2)
        self.calculator.divide()

        self.divider.calc.assert_called_with(1, 2)


