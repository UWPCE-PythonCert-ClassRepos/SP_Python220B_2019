'''unit testing the main program as a whole'''
import sys
sys.path.append("./inventory_management")
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.market_prices import get_latest_price
import inventory_management.main as main

class ModuleTests(TestCase):

    def test_module(self):
        '''build a inventory and then test retrieval of items'''

        main.FULL_INVENTORY = {}
        first_item = ['SOFA', 'Sectional', 100, 'n', 'n']
        new_e_item = ['MICWV', 'Microwave', 10, 'n', 'y', 'Whirlpool', '1000V']
        new_f_item = ['DINE_TBL', 'Dining Table', 50, 'y', 'wood', 'L']
        test_inventory = {'SOFA': {'description': 'Sectional', 'market_price': 24,
                                   'product_code': 'SOFA', 'rental_price': 100},
                          'DINE_TBL': {'description': 'Dining Table', 'market_price': 24,
                                       'material': 'wood', 'product_code': 'DINE_TBL',
                                       'rental_price': 50, 'size': 'L'},
                          'MICWV': {'brand': 'Whirlpool', 'description': 'Microwave',
                                    'market_price': 24, 'product_code': 'MICWV',
                                    'rental_price': 10, 'voltage': '1000V'}}
        get_item_sofa = '''product_code:SOFA
description:Sectional
market_price:24
rental_price:100
'''
        get_item_micwv = '''product_code:MICWV
description:Microwave
market_price:24
rental_price:10
brand:Whirlpool
voltage:1000V
'''

        with patch('builtins.input', side_effect=first_item):
            main.add_new_item()
        with patch('builtins.input', side_effect=new_e_item):
            main.add_new_item()
        with patch('builtins.input', side_effect=new_f_item):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, test_inventory)

        with patch('builtins.input', side_effect=['SOFA']):
            with patch('sys.stdout', new=StringIO()) as result:
                main.item_info()
                self.assertEqual(result.getvalue(), get_item_sofa)

        with patch('builtins.input', side_effect=['MICWV']):
            with patch('sys.stdout', new=StringIO()) as result:
                main.item_info()
                self.assertEqual(result.getvalue(), get_item_micwv)
