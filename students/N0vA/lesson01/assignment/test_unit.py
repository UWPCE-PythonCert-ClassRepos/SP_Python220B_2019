"""
Unit Tests for Inventory Management.
"""
import sys
sys.path.append('inventory_management')
# Test libs
from unittest import TestCase
from unittest.mock import patch, MagicMock
# Import modules
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
import inventory_management.market_prices as market_prices
import inventory_management.main as main


class InventoryTests(TestCase):
    """Class to test inventory class."""

    def test_inventory(self): # Testing inventory functionality
        
        record = Inventory('2203', 'speaker', 500, 225)
        expected = {'product_code': '2203',
                    'description': 'speaker',
                    'market_price': 500,
                    'rental_price': 225}
        
        # Test assertions
        self.assertEqual(expected, record.return_as_dictionary())
        self.assertEqual('2203', record.product_code)
        self.assertEqual('speaker', record.description)
        self.assertEqual(500, record.market_price)
        self.assertEqual(225, record.rental_price)

class ElectricAppliancesTests(TestCase):
    """Class to test Electric Appliance class."""

    def test_ea(self): # Test functionality of Electric Appliance module."""

        record = ElectricAppliances('1547', 'monitor', 400,
                                    210, 'Acer', 200)
        expected = {'product_code': '1547',
                    'description': 'monitor',
                    'market_price': 400,
                    'rental_price': 210,
                    'brand': 'Acer',
                    'voltage': 200}

        # Test Assertions
        self.assertEqual(expected, record.return_as_dictionary())
        self.assertEqual('1547', record.product_code)
        self.assertEqual('monitor', record.description)
        self.assertEqual(400, record.market_price)
        self.assertEqual(210, record.rental_price)
        self.assertEqual('Acer', record.brand)
        self.assertEqual(200, record.voltage)

class FurnitureTests(TestCase):
    """Class to test Furniture class."""
    
    def test_furniture(self): # Tests furniture class functionality.

        record = Furniture('0682', 'chair', 150, 85, 'leather', '54 x 42')
        expected = {'product_code': '0682',
                    'description': 'chair',
                    'market_price': 150,
                    'rental_price': 85,
                    'material': 'leather',
                    'size': '54 x 42'}

        # Test Assertions
        self.assertEqual(expected, record.return_as_dictionary())
        self.assertEqual('leather', record.material)
        self.assertEqual('54 x 42', record.size)
        
class MarketPrciesTest(TestCase):
    """Tests module for market prices."""
    def test_market_prices(self):
        self.assertEqual(24, market_prices.get_latest_price(24))

class MainTests(TestCase):
    """Class to test main menu functionality."""

    def test_main_menu(self): # Tests main menu setup
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_get_price(self): # Test get_price - use mock method

        self.get_price = MagicMock(return_value=24)
        self.assertEqual(main.get_price(5), print('Get price'))

    def test_add_new_item(self):
        """Tests program to add new item to inventory."""

        # Prep test cases for each type of new item
        inv_1 = ['2203', 'speaker', 225, 'n', 'n']
        furn_1 = ['0682', 'chair', 85, 'y', 'leather', '54 x 42']
        ea_1 = ['1547', 'monitor', 210, 'N', 'Y', 'Acer', 200]

        # Check if new item is added for inventory
        with patch('market_prices.get_latest_price', return_value=500):
            with patch('builtins.input', side_effect=inv_1):
                inv_dict = {}
                main.FULL_INVENTORY = {}
                main.add_new_item()
                inv_dict['2203'] = {'product_code': '2203',
                                    'description': 'speaker',
                                    'market_price': 500,
                                    'rental_price': 225
                                    }

                self.assertEqual(inv_dict, main.FULL_INVENTORY)

        # Check if new item is added for furniture
        with patch('market_prices.get_latest_price', return_value=150):
            with patch('builtins.input', side_effect=furn_1):
                furn_dict = {}
                main.FULL_INVENTORY = {}
                main.add_new_item()
                furn_dict['0682'] = {'product_code': '0682',
                                    'description': 'chair',
                                    'market_price': 150,
                                    'rental_price': 85,
                                    'material': 'leather',
                                    'size': '54 x 42'
                                    }

                self.assertEqual(furn_dict, main.FULL_INVENTORY)

        # Check if new item is added for electric appliances
        with patch('market_prices.get_latest_price', return_value=400):
            with patch('builtins.input', side_effect=ea_1):
                ea_dict = {}
                main.FULL_INVENTORY = {}
                main.add_new_item()
                ea_dict['1547'] = {'product_code': '1547',
                                    'description': 'monitor',
                                    'market_price': 400,
                                    'rental_price': 210,
                                    'brand': 'Acer',
                                    'voltage': 200
                                    }

                self.assertEqual(ea_dict, main.FULL_INVENTORY)

    def test_item_info(self):
        """Tests functionality of program to get item info."""

        expected = {'product_code': '5491',
                    'description': 'computer',
                    'market_price': 1650,
                    'rental_price': 1250}

        with patch('builtins.input', side_effect=['5491']):
            self.assertEqual(main.item_info(), print(expected))

    def test_item_info_select(self):
        """Select item info from a dictionary of items."""

        main.FULL_INVENTORY = {}
        expected =  {
            '0430': {'product_code': '0430',
                     'description': 'desk',
                     'market_price': 600,
                     'rental_price': 375,
                     'material': 'wood',
                     'size': '30 x 72'},
            '1011': {'product_code': '1011',
                     'description': 'printer',
                     'market_price': 2000,
                     'rental_price': 950,
                     'brand': 'HP',
                     'voltage': 750},
            '0885': {'product_code': '0885',
                     'description': 'headphones',
                     'market_price': 295,
                     'rental_price': 105},
                    }
        main.FULL_INVENTORY = expected

        # Get item info from selected item
        with patch('builtins.input', side_effect=['1011']):
            self.assertEqual(main.item_info(), print(expected.get('1011')))
            self.assertEqual(main.FULL_INVENTORY['1011'], expected.get('1011'))

    def test_exit_program(self):
        """Tests functionality program will close."""
        with self.assertRaises(SystemExit):
            main.exit_program()    