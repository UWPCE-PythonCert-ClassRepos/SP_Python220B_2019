'''Integration testing for the inventory management system'''

from unittest import TestCase
from unittest.mock import patch
import sys
sys.path.append('inventory_management')
import inventory_management.main as main

# pylint: disable = C0413

TEST_DICT = {'I123': {'product_code': 'I123',
                      'description': 'Thingabob',
                      'market_price': 24,
                      'rental_price': 4.99},
             'C234': {'product_code': 'C234',
                      'description': 'chair',
                      'market_price': 24,
                      'rental_price': 39.99,
                      'material': 'wood',
                      'size': 'X-Large'},
             'E345': {'product_code': 'E345',
                      'description': 'refrigerator',
                      'market_price': 24,
                      'rental_price': 145.99,
                      'brand': 'GE',
                      'voltage': 110}}

class TestIntegration(TestCase):
    '''Tests the integrated inventory management system'''

    def test_add_new_item(self):
        '''Tests the add_new_item function'''

        # User inputs
        test_inventory = ['I123', 'Thingabob', 4.99, 'n', 'n']
        test_furniture = ['C234', 'chair', 39.99, 'y', 'wood', 'X-Large']
        test_elect_app = ['E345', 'refrigerator', 145.99, 'n', 'y', 'GE', 110]

        # Tests adding an inventory item
        with patch('builtins.input', side_effect=test_inventory):
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY['I123'], TEST_DICT['I123'])

        # Tests adding a furniture item
        with patch('builtins.input', side_effect=test_furniture):
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY['C234'], TEST_DICT['C234'])

        # Tests adding an electrical appliance item
        with patch('builtins.input', side_effect=test_elect_app):
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY['E345'], TEST_DICT['E345'])

    def test_item_info(self):
        '''Tests the item_info function'''

        main.FULL_INVENTORY = TEST_DICT

        # Tests item info for an inventory item
        with patch('builtins.input', side_effect='I123'):
            self.assertEqual(main.FULL_INVENTORY['I123'], TEST_DICT.get('I123'))

        # Tests item info for a furniture item
        with patch('builtins.input', side_effect='C234'):
            self.assertEqual(main.FULL_INVENTORY['C234'], TEST_DICT.get('C234'))

        # Tests item info for an electrical appliance item
        with patch('builtins.input', side_effect='E345'):
            self.assertEqual(main.FULL_INVENTORY['E345'], TEST_DICT.get('E345'))

        # Tests the correct return for an item not in the inventory
        with patch('builtins.input', side_effect=['Z789']):
            self.assertEqual(main.item_info(), print('Item not found in inventory'))

    def test_exit_program(self):
        '''Tests the exit_program function'''

        with self.assertRaises(SystemExit):
            main.exit_program()
