from unittest import TestCase
#from unittest.mock import MagicMock
from unittest.mock import patch
import io

from inventory_management.main import main_menu,  get_price, add_new_item
from inventory_management.main import item_info, exit_program, FULL_INVENTORY
#from inventory_management.market_prices import get_latest_price
#from inventory_management.inventory_class import Inventory
#from inventory_management.furniture_class import Furniture
#from inventory_management.electric_appliances_class import ElectricAppliances


class InvManIntegrationTest(TestCase):

    def test_whole_system(self):

        #input_inventory = ('K2', 'Snowboard', 1000, 10)
        input_list = [('OL1', 'OLED TV', 2000, 'n', 'y', 'LG', 110), 
                      ('C1', 'Lounge Chair', 1000, 'y', 'Brass', 'L'),
                      ('K2', 'Snowboard', 1000, 'n', 'n')
                      ]
        gold_list = [{'productCode': 'OL1', 'description': 'OLED TV', 
                    'marketPrice': 24, 'rentalPrice': 2000, 'brand': 'LG', 
                    'voltage': 110},
                    {'productCode': 'C1', 'description': 'Lounge Chair', 
                    'marketPrice': 24, 'rentalPrice': 1000, 'material': 'Brass', 
                    'size': 'L'},
                    {'productCode': 'K2', 'description': 'Snowboard', 
                    'marketPrice': 24, 'rentalPrice': 1000}
        ]

        print_out = '''productCode:OL1
description:OLED TV
marketPrice:24
rentalPrice:2000
brand:LG
voltage:110
'''

        #add a new item
        with patch('builtins.input', side_effect='1'):
            main_menu()
            with patch('builtins.input', side_effect=input_list[0]):
                add_new_item()
                self.assertDictEqual(gold_list[0], FULL_INVENTORY['OL1'])

        #print the item in inventory
        with patch('builtins.input', side_effect='2'):
            main_menu()
            with patch('builtins.input', side_effect=input_list[0]):
                with patch('sys.stdout', new=io.StringIO()) as actual_result:
                    item_info()
            self.assertEqual(actual_result.getvalue(), print_out)

        #then quit
        with patch('builtins.input', side_effect='q'):
            main_menu()
            with self.assertRaises(SystemExit):
                exit_program()
