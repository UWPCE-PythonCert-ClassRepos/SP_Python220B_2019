"""
Tests inegrated code
"""
from unittest import TestCase
from unittest import mock

from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price
from inventory_management.main import main_menu
from inventory_management.main import add_new_item
from inventory_management.main import item_info
from inventory_management.main import exit_program
from inventory_management.main import FULL_INVENTORY

class integration_test(TestCase):
    """
    Class setup for integrated code test
    """
    def test_integ(self):
        """
        Tests adding a furniture class and electric appliances class to the global full_inventory
        """
        with mock.patch('builtins.input', side_effect = ['300', 'shirt', '500', 'y', 'cotton', 'S']):
            add_new_item()
            self.assertEqual(FULL_INVENTORY['300'], {'product_code': '300',
                                        'description': 'shirt',
                                        'market_price': 24,
                                        'rental_price': '500',
                                        'material': 'cotton',
                                        'size': 'S'})
        with mock.patch('builtins.input', side_effect = ['200', 'machine', '500', 'n', 'y', 'ACE', '12']):
            add_new_item()
            self.assertEqual(FULL_INVENTORY['200'], {'product_code': '200',
                                        'description': 'machine',
                                        'market_price': 24,
                                        'rental_price': '500',
                                        'brand': 'ACE',
                                        'voltage': '12'})
        self.assertEqual(FULL_INVENTORY, {'300':{'product_code': '300',
                                        'description': 'shirt',
                                        'market_price': 24,
                                        'rental_price': '500',
                                        'material': 'cotton',
                                        'size': 'S'},
                                        '200':{'product_code': '200',
                                        'description': 'machine',
                                        'market_price': 24,
                                        'rental_price': '500',
                                        'brand': 'ACE',
                                        'voltage': '12'}})
