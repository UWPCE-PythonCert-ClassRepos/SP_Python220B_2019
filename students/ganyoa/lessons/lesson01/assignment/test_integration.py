import sys
import io

from unittest import TestCase
from unittest.mock import patch, MagicMock

import inventory_management.main as main
import inventory_management.market_prices as mp
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory

class IntegrationTest(TestCase):

    def test_main(self):
        '''
        tests a typical sequence of a user entering two new items
        each mock starts with user input 1 for add new item to inventory
        followed by details for a piece of furniture then appliance
        lastly a mock looks up item info for item 001
        '''
        with patch('builtins.input', side_effect=('1', '001', 'bench', 63, 'y', 'wood', 'XL')):
            main.main_menu()()
            self.assertEqual(main.FULL_INVENTORY, {'001': {'product_code': '001',
                                                       'description': 'bench',
                                                       'market_price': 24,
                                                       'rental_price': 63,
                                                       'material': 'wood',
                                                       'size': 'XL'}})

        with patch('builtins.input', side_effect=('1', '024', 'tv', 299, 'n', 'y', 'tvsrus', 110)):
            with patch('inventory_management.market_prices.get_latest_price', return_value=859):
                main.main_menu()()
            self.assertEqual(main.FULL_INVENTORY, {'001': {'product_code': '001',
                                                        'description': 'bench',
                                                        'market_price': 24,
                                                        'rental_price': 63,
                                                        'material': 'wood',
                                                        'size': 'XL'},
                                                   '024': {'product_code': '024',
                                                        'description': 'tv',
                                                        'market_price': 859,
                                                        'rental_price': 299,
                                                        'brand': 'tvsrus',
                                                        'voltage': 110}})

        with patch('builtins.input', side_effect = ['001']):
            with patch('sys.stdout', new = io.StringIO() ) as input_result:
                main.item_info()
        self.assertEqual(input_result.getvalue(), 'product_code:001\n'
                                                  'description:bench\n'
                                                  'market_price:24\n'
                                                  'rental_price:63\n'
                                                  'material:wood\n'
                                                  'size:XL\n')
