# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 17:37:53 2019

@author: Humberto
"""

from unittest import TestCase
from unittest.mock import patch
import io

import inventory_management.main as main
from inventory_management.main import main_menu, get_price, add_new_item
from inventory_management.main import item_info, exit_program, FULL_INVENTORY
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.inventory_class import Inventory
import inventory_management.market_prices as market_prices


Class TestInventoryIntegration(TestCase):
    
    def test_integration(self):
        
        main.FULL_INVENTORY = {}
        
        compare = {
                'N64':{'productCode':'B33',
                   'description':'Nutri-Bullet Blender',
                   'marketPrice':24,
                   'rentalPrice':25,
                   'brand':'Nutri-Bullet',
                   'voltage':12}
                'C74':{'productCode':'C74',
                   'description':'IKEA Malmer Couch',
                   'marketPrice':24,
                   'rentalPrice':125,
                   'material':'Leather',
                   'size':'L'}
                }
        
        item_inputs = [['C74','IKEA Malmer Couch',650,'y','Leather','L'],
                       ['B33','Nutri-Bullet Blender',100,'y','y','Nutri-Bullet',12]]
        
        with patch('builtins.input', side_effect=item_inputs[0]):
            main.add_new_item()
            
        with patch('builtins.input', side_effect=item_inputs[1]):
            main.add_new_item()
        
        self.assertEqual(main.FULL_INVENTORY,compare)