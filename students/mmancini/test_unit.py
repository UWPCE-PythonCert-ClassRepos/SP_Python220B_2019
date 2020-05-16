#!/usr/bin/env python3

"""
Unit Testing Inventory Management
"""

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

import inventory_management.market_prices as market_prices
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

            
    def test_get_price_1(self):
        """Test get_price"""

        self.assertEqual(main.get_price('test'), 24)


    def test_get_price_2(self):
        """ Test get_price mocked return """

        self.mp.get_latest_price = MagicMock(return_value=50)
        self.assertEqual(main.get_price('test'), 50)
    
