import unittest
import sys

sys.path.append('inventory_management')

from inventory_class import Inventory
from electric_appliances_class import ElectricAppliances
from furniture_class import Furniture
from market_prices import get_latest_price
import main as main
from unittest.mock import patch

class InventoryTest(unittest.TestCase):
    """Test cases for inventory_class module"""
    def test_inventory_class(self):
        """Test the Inventory instantiation and return_as_dictionary() method"""
        expected = {'item_code': 'DRYWALL',
                    'description': 'Just an ordinary drywall board.  Pretty boring.',
                    'market_price': '100.00',
                    'rental_price': '8.00'}

        item_attributes = {'item_code': 'DRYWALL',
                           'description': 'Just an ordinary drywall board.  Pretty boring.',
                           'market_price': '100.00',
                           'rental_price': '8.00'}

        self.item = Inventory(**item_attributes)

        self.assertIsInstance(self.item, Inventory)

        self.assertEqual(expected, self.item.return_as_dictionary())

class ElectricApplianceTest(unittest.TestCase):
    """Test cases for electric_appliances_class module"""
    def test_electric_appliances_class(self):
        """Test the ElectricAppliances instantiation and return_as_directory() method"""
        expected = {'item_code': 'OVEN',
                    'description': 'A great double oven',
                    'market_price': '599.99',
                    'rental_price': '40.00',
                    'brand': 'GT',
                    'voltage': '240V'}


        item_attributes = {'item_code': 'OVEN',
                           'description': 'A great double oven',
                           'market_price': '599.99',
                           'rental_price': '40.00',
                           'brand': 'GT',
                           'voltage': '240V'}

        self.item = ElectricAppliances(**item_attributes)

        self.assertIsInstance(self.item, Inventory, ElectricAppliances)

        self.assertEqual(expected, self.item.return_as_dictionary())

class FurnitureTest(unittest.TestCase):
    """Test cases for furniture_class module"""
    def test_electric_appliances_class(self):
        """Test the ElectricAppliances instantiation and return_as_directory() method"""
        expected = {'item_code': 'SECTIONAL',
                    'description': 'A pleather sectional sofa',
                    'market_price': '1045.87',
                    'rental_price': '102.77',
                    'material': 'Pleather',
                    'size': 'XL'}


        item_attributes = {'item_code': 'SECTIONAL',
                           'description': 'A pleather sectional sofa',
                           'market_price': '1045.87',
                           'rental_price': '102.77',
                           'material': 'Pleather',
                           'size': 'XL'}

        self.item = Furniture(**item_attributes)

        self.assertIsInstance(self.item, Inventory, Furniture)

        self.assertEqual(expected, self.item.return_as_dictionary())

class MarketPricesTest(unittest.TestCase):
    """Test cases for market_prices module"""
    def test_market_prices(self):
        """Test the get_latest_price() method"""
        self.assertEqual(24, get_latest_price('SECTIONAL'))

class MainTest(unittest.TestCase):
    """Test cases for main module"""
    def test_menu(self):
        """Test the main_menu() method"""
        with patch('builtins.input', side_effect=['1']):
            self.assertEqual(main.main_menu(), main.add_new_item)

        with patch('builtins.input', side_effect=['2']):
            self.assertEqual(main.main_menu(), main.item_info)

        with patch('builtins.input', side_effect=['q']):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_add_item(self):
        """Test the add_new_item() method"""
        with patch('builtins.input', side_effect=['BOOK', 'A book', '2.50', 'n', 'n']):
            main.add_new_item()
            self.assertEqual(main.INVENTORY_DATA['BOOK'], {'item_code': 'BOOK',
                                                           'description': 'A book',
                                                           'market_price': 24,
                                                           'rental_price': '2.50'})

        with patch('builtins.input', side_effect=['KITCHAIR', 'Kitchen chair', '4.22', 'y', 'Wood', 'M']):
            main.add_new_item()
            self.assertEqual(main.INVENTORY_DATA['KITCHAIR'], {'item_code': 'KITCHAIR',
                                                               'description': 'Kitchen chair',
                                                               'market_price': 24,
                                                               'rental_price': '4.22',
                                                               'material': 'Wood',
                                                               'size': 'M'})

        with patch('builtins.input', side_effect=['DISH2K', 'Dishwasher with coffee maker',
                                                  '9.55', 'n', 'y', 'Boosh', '120V']):
            main.add_new_item()
            self.assertEqual(main.INVENTORY_DATA['DISH2K'], {'item_code': 'DISH2K',
                                                             'description': 'Dishwasher with coffee maker',
                                                             'market_price': 24,
                                                             'rental_price': '9.55',
                                                             'brand': 'Boosh',
                                                             'voltage': '120V'})

    def test_get_price(self):
        """Test the get_price() method"""
        self.assertEqual(main.get_price('DISH2K'), 'Current price of DISH2K: 24')

    def test_item_info(self):
        """Test the item_info() method"""
        with patch('builtins.input', side_effect=['DISH2K']):
            #Test the valid key case
            self.assertEqual(None, main.item_info())
        with patch('builtins.input', side_effect=['DISH3K']):
            #Test the invalid key case
            self.assertEqual(None, main.item_info())


    def test_exit_program(self):
        """Test the exit_program() method"""
        with self.assertRaises(SystemExit):
            main.exit_program()
