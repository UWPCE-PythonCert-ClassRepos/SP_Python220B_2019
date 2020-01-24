from unittest import TestCase
from unittest.mock import patch
import sys

sys.path.append('inventory_management')

import main

class IntegrationTest(TestCase):
    """Integration test cases"""
    def test_integration(self):
        """Test the integrated application"""
        expected_inventory = {'64': {'item_code': '64', 'description': 'Nintendo 64',
                                    'market_price': 24, 'rental_price': '5.64'},
                              'WD': {'item_code': 'WD', 'description': 'Combo washer/dryer',
                                     'market_price': 24, 'rental_price': '13.75',
                                     'brand': 'Baytag', 'voltage': '240V'},
                              'DINTAB': {'item_code': 'DINTAB', 'description': 'Dining table',
                                         'market_price': 24, 'rental_price': '7.99',
                                         'material': 'Stainless steel', 'size': 'L'}}
        with patch('builtins.input', side_effect=['64', 'Nintendo 64', '5.64', 'n', 'n']):
            main.add_new_item()
        with patch('builtins.input', side_effect=['WD', 'Combo washer/dryer', '13.75', 'n', 'y',
                                                  'Baytag', '240V']):
            main.add_new_item()
        with patch('builtins.input', side_effect=['DINTAB', 'Dining table', '7.99', 'y',
                                                  'Stainless steel', 'L']):
            main.add_new_item()
        with patch('builtins.input', side_effect=['2']):
            self.assertEqual(main.main_menu(), main.item_info)
        self.assertEqual(expected_inventory, main.INVENTORY_DATA)
