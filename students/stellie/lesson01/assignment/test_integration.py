# Stella Kim
# Assignment 1: Advanced Testing

"""Integration tests for inventory management system"""

from unittest import TestCase
from unittest.mock import patch
import inventory_management.main as main


class ModuleTests(TestCase):
    """Class for inventory system integration testing"""

    def test_menu_inventory(self):
        """Test output of inventory using mock input data"""
        item_1 = [6, 'Rice Cooker', 15, 'N', 'Y', 'Tiger', 220]
        item_2 = [7, 'Piano', 1000, 'Y', 'Wood', 'L']
        item_3 = [8, 'Towels', 5, 'N', 'N']

        test_dict = {6: {'product_code': 6,
                         'description': 'Rice Cooker',
                         'market_price': 24,
                         'rental_price': 15,
                         'brand': 'Tiger',
                         'voltage': 220},
                     7: {'product_code': 7,
                         'description': 'Piano',
                         'market_price': 24,
                         'rental_price': 1000,
                         'material': 'Wood',
                         'size': 'L'},
                     8: {'product_code': 8,
                         'description': 'Towels',
                         'market_price': 24,
                         'rental_price': 5}}

        with patch('builtins.input', side_effect=item_1):
            main.add_new_item()
        with patch('builtins.input', side_effect=item_2):
            main.add_new_item()
        with patch('builtins.input', side_effect=item_3):
            main.add_new_item()

        self.assertEqual(main.FULL_INVENTORY[6], test_dict[6])
        self.assertEqual(main.FULL_INVENTORY[7], test_dict[7])
        self.assertEqual(main.FULL_INVENTORY[8], test_dict[8])

    def test_item_info(self):
        """Test correct output for requested item lookup"""
        main.FULL_INVENTORY = {9: {'product_code': 9,
                                   'description': 'TV',
                                   'market_price': 500,
                                   'rental_price': 75,
                                   'brand': 'LG',
                                   'voltage': 120}}

        with patch('builtins.input', side_effect=[9]):
            self.assertEqual(main.item_info(),
                             print(main.FULL_INVENTORY.get(9)))
            self.assertEqual(main.FULL_INVENTORY[9],
                             main.FULL_INVENTORY.get(9))

    def test_exit_program(self):
        """Test for raised exception if system does not exit properly"""
        with self.assertRaises(SystemExit):
            main.exit_program()
