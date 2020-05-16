#!/usr/bin/env python3

"""
Unit Testing Inventory Management
"""

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

import inventory_management.market_prices as market_prices
from inventory_management.inventory_class import Inventory
import inventory_management.main as main


class MainTests(TestCase):
    """ test main """

    def setUp(self):
        """ setup """
        self.main = main
        self.mp = market_prices
		
		
    def test_main_menu(self):
        """Test that the user inputs"""

        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)
            
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

            
    def test_get_price(self):
        """Test get_price"""

        self.assertEqual(main.get_price('test'), 24)

        
class InventoryClassTests(TestCase):
    """ test for inventory """
    def setUp(self):
        '''creates inventory object'''
        self.inventory = Inventory(1, 'some description', 25, 10.50)

    def test_inventory_init(self):
        '''tests init values for inventory object'''
        assert self.inventory.product_code == 1
        assert self.inventory.description == 'some description'
        assert self.inventory.market_price == 25
        assert self.inventory.rental_price == 10.50

    def test_return_as_dict(self):
        '''tests the return as dict method in class inventory'''
        inventory_dict = self.inventory.return_as_dictionary()
        assert inventory_dict == {'product_code': 1,
                                  'description': 'some description',
                                  'market_price': 25,
                                  'rental_price': 10.50}
        
class TestMarketPrices(TestCase):
    """ test market_prices return value """

    def setUp(self):
        """ setup """
        self.main = main
        self.mp = market_prices

    def test_get_latest_price(self):
        """ Test get_latest_price mocked return val """

        self.mp.get_latest_price = MagicMock(return_value=50)
        self.assertEqual(50, self.mp.get_latest_price(50))
