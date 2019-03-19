"""Creates a full suite of tests for all classes in inventory_management"""

import sys
sys.path.append('/Users/allth/OneDrive/Desktop/Python/Python220/'
                'SP_Python220B_2019/students/dfspray/Lesson01/inventory_management')
import unittest
import unittest.mock
from unittest.mock import MagicMock
from unittest.mock import patch
import inventory_management.market_prices as market_prices
import inventory_management.main as main
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory

class TestInventoryClass(unittest.TestCase):
    """Write a class that tests inventory_class.py"""
    def test_inventory(self):
        """Test the inventory successfully stores an item"""
        test_info1 = [1, "shoe", 10, 20]
        test_inventory = Inventory(test_info1)
        expected_dict = {
            'product_code': 1,
            'description': "shoe",
            'market_price': 10,
            'rental_price': 20
        }
        actual_dict = test_inventory.return_as_dictionary()
        self.assertEqual(actual_dict, expected_dict)

class TestElectricAppliancesClass(unittest.TestCase):
    """Write a class that tests all of electric_appliances_class.py"""
    def test_appliances_dictionary(self):
        """Test the user can store an electric appliance"""
        test_info2 = [2, "cable", 25, 50]
        test_appliance = ElectricAppliances(test_info2, "honeywell", 10)
        expected_dict = {
            'product_code': 2,
            'description': "cable",
            'market_price': 25,
            'rental_price': 50,
            'brand': "honeywell",
            'voltage': 10
        }
        actual_dict = test_appliance.return_as_dictionary()
        self.assertEqual(actual_dict, expected_dict)

class TestFurnitureClass(unittest.TestCase):
    """Write a class that tests all of furniture_class.py"""
    def test_furniture_dictionary(self):
        """Test the user can store a furniture item"""
        test_info3 = [3, "chair", 20, 40]
        test_furniture = Furniture(test_info3, "leather", 100)
        expected_dict = {
            'product_code': 3,
            'description': "chair",
            'market_price': 20,
            'rental_price': 40,
            'material': "leather",
            'size': 100
        }
        actual_dict = test_furniture.return_as_dictionary()
        self.assertEqual(actual_dict, expected_dict)

class TestMarketPrices(unittest.TestCase):
    """Write a class that tests all of market_prices.py"""
    def test_get_latest_price(self):
        """Test the user can retrieve the latest market price"""
        market_prices.get_latest_price = MagicMock(return_value=24)
        actual_price = market_prices.get_latest_price(1)
        expected_price = 24
        market_prices.get_latest_price.assert_called_with(1)
        self.assertEqual(actual_price, expected_price)

class TestMain(unittest.TestCase):
    """Write a class that tests all the main.py"""

    def test_main_menu(self):
        """Test that the inputs on the main menu function properly"""
        expected_selection1 = 'add_new_item'
        with patch('builtins.input', side_effect='1'):
            actual_selection1 = main.main_menu()
        self.assertEqual(actual_selection1.__name__, expected_selection1)

        expected_selection2 = 'item_info'
        with patch('builtins.input', side_effect='2'):
            actual_selection2 = main.main_menu()
        self.assertEqual(actual_selection2.__name__, expected_selection2)

        expected_selection3 = 'exit_program'
        with patch('builtins.input', side_effect='q'):
            actual_selection3 = main.main_menu()
        self.assertEqual(actual_selection3.__name__, expected_selection3)

    def test_get_price(self):
        """Test that the user can get the market price"""
        actual = main.get_price(1)
        expected = 24
        self.assertEqual(actual, expected)

    def test_add_new_item(self):
        """Test that user can add a new item to inventory"""
        input_item1 = ['1', 'chair', '10', 'y', 'wood', 'S']
        with patch('builtins.input', side_effect=input_item1):
            main.add_new_item()

        input_item2 = ['2', 'toaster', '20', 'n', 'y', 'Ferrari', '200']
        with patch('builtins.input', side_effect=input_item2):
            main.add_new_item()

        input_item3 = ['3', 'paper', '30', 'n', 'n']
        with patch('builtins.input', side_effect=input_item3):
            main.add_new_item()

        test_dictionary = {
            '1':{'product_code': '1', 'description': 'chair', 'market_price': 24,
                 'rental_price': '10', 'material': 'wood', 'size': 'S'},
            '2':{'product_code': '2', 'description': 'toaster', 'market_price': 24,
                 'rental_price': '20', 'brand': 'Ferrari', 'voltage': '200'},
            '3':{'product_code': '3', 'description': 'paper', 'market_price': 24,
                 'rental_price': '30'}
        }

        self.assertEqual(test_dictionary, main.return_full_inventory())

    def test_item_info(self):
        """Test user can get retrieve item info"""
        input_item4 = ['1', 'chair', '10', 'y', 'wood', 'S']
        with patch('builtins.input', side_effect=input_item4):
            main.add_new_item()

        with patch('builtins.input', side_effect='1'):
            actual_info1 = main.item_info()
        expected_info1 = '''product_code:1
description:chair
market_price:24
rental_price:10
material:wood
size:S'''
        self.assertEqual(actual_info1, expected_info1)

        with patch('builtins.input', side_effect='0'):
            actual_info2 = main.item_info()
        expected_info2 = "Item not found in inventory"
        self.assertEqual(actual_info2, expected_info2)

    def test_exit(self):
        """Test if exit_program exits the program successfully"""
        with self.assertRaises(SystemExit):
            main.exit_program()

if __name__ == '__main__':
    unittest.main()
	 