import sys
import os
# locate file path
sys.path.append('inventory_management')
from unittest import TestCase
from unittest.mock import patch, MagicMock
from inventory_management.inventory_class import Inventory 
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
import inventory_management.market_prices as market_prices
import inventory_management.main as main

class TestInventoryManagement(TestCase):
    def test_integration(self):
        main.FULLINVENTORY = {}
        inv_obj_1 = ['545', 'pan', 13.0, 'n', 'n']
        furn_obj_1 = ['0455', 'couch', 30.0, 'y', 'leather', 'L']
        elec_app_1 = ['786', 'phone charger', 'n', 'y', 'apple', 130.0]

        inventory_dict = {'product_code': '545',
                          'description': 'pan',
                          'market_price': 42.0,
                          'rental_price': 13.0}
        furniture_dict = {'product_code': '0455',
                          'description': 'couch',
                          'market_prices': 280.0,
                          'rental_price': 30.0,
                          'material': 'leather',
                          'size': 'L'}
        electrical_dict = {'product_code': '786',
                           'description': 'phone charger',
                           'market_price': 400.0,
                           'rental_price': 130.0,
                           'brand': 'apple',
                           'voltage': 2.9}
        
        main.FULL_INVENTORY = {}

        # add items to the inventory

        with patch('builtins.input', side_effect=inv_obj_1):
            with patch('market_prices.get_latest_price', return_value=42.0):
                main.add_new_item()
        
        with patch('builtins.input', side_effect=elec_app_1):
            with patch('market_prices.get_latest_price', return_value=400.0):
                main.add_new_item()

        with patch('builtins.input', side_effect=furn_obj_1):
            with patch('market_prices.get_latest_price', return_value=280.0):
                main.add_new_item()

        print(main.FULL_INVENTORY)
