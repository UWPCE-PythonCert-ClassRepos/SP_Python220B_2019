import sys
sys.path.append('inventory_management')
import inventory_management.main as main
from unittest import TestCase
from unittest.mock import patch

class InventoryManagementTest(TestCase):
    """ Tests Inventory Management as a whole """

    def test_inventory(self):
        """ Test adding inventory """

        main.full_inventory = {}

        generic_input = [1, 'generic', 10, 'n', 'n']
        furniture_input = [2, 'furniture', 10, 'y', 'Upholstery', 'L']
        electric_input = [3, 'electric', 10, 'n', 'y', 'Samsung', 120]
        
        final_dict = {1: {'product_code': 1,
                          'description': 'generic',
                          'market_price': 24,
                          'rental_price': 10},
                      2: {'product_code': 2,
                          'description': 'furniture',
                          'market_price': 24,
                          'rental_price': 10,
                          'material': 'Upholstery',
                          'size': 'L'},
                      3: {'product_code': 3,
                          'description': 'electric',
                          'market_price': 24,
                          'rental_price': 10,
                          'brand': 'Samsung',
                          'voltage': 120}}

        with patch('builtins.input', side_effect=generic_input):
            main.add_new_item()

        with patch('builtins.input', side_effect=furniture_input):
            main.add_new_item()

        with patch('builtins.input', side_effect=electric_input):
            main.add_new_item()

        self.assertEqual(main.full_inventory, final_dict)
