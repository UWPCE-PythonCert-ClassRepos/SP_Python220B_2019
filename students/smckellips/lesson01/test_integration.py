'''Unit testing module for inventory_management'''
import os
import sys
from unittest import TestCase
from unittest.mock import patch, MagicMock

sys.path.append('./inventory_management')
import inventory_management.main as main
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
from inventory_management.market_prices import get_latest_price


class ModuleTests(TestCase):

    def test_moduletest(self):
        main.FULL_INVENTORY = {}

        inventory_input_params = ['Code4', 'Item4 Test', 4, 'n', 'n' ]
        electric_input_params = ['Code5', 'Item5 Test', 5, 'n', 'y', 'BrandB', 120]
        furniture_input_params = ['Code6', 'Item6 Test', 6, 'y', 'MaterialA', 'S']
        target_inventory ={ 
            'Code4': 
                {
                    'product_code': 'Code4',
                    'description': 'Item4 Test',
                    'market_price' : 'Code4',
                    'rental_price' : 4
                }
            ,
            'Code5': 
                {
                    'product_code': 'Code5',
                    'description': 'Item5 Test',
                    'market_price' : 'Code5',
                    'rental_price' : 5,
                    'brand': 'BrandB',
                    'voltage': 120
                }
            ,
            'Code6': 
                {
                    'product_code': 'Code6',
                    'description': 'Item6 Test',
                    'market_price' : 'Code6',
                    'rental_price' : 6,
                    'material': 'MaterialA',
                    'size': 'S'
                }
        }

        with patch('builtins.input', side_effect=inventory_input_params):
            main.add_new_item()
        with patch('builtins.input', side_effect=electric_input_params):
            main.add_new_item()
        with patch('builtins.input', side_effect=furniture_input_params):
            main.add_new_item()

        self.assertEqual(main.FULL_INVENTORY, target_inventory)
