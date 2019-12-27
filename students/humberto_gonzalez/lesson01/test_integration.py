# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 17:37:53 2019

@author: Humberto
"""

from unittest import TestCase
from unittest.mock import patch
import inventory_management.main as main

class TestInventoryIntegration(TestCase):
    """Tests overall integration"""
    def test_integration(self):
        """Tests the full integration of the fnctions"""
        main.FULL_INVENTORY = {}
        compare = {'B33':{'productCode':'B33',
                          'description':'Nutri-Bullet Blender',
                          'marketPrice':24,
                          'rentalPrice':25,
                          'brand':'Nutri-Bullet',
                          'voltage':12},
                   'C74':{'productCode':'C74',
                          'description':'IKEA Malmer Couch',
                          'marketPrice':24,
                          'rentalPrice':125,
                          'material':'Leather',
                          'size':'L'}}
        item_inputs = [['C74', 'IKEA Malmer Couch', 125, 'y', 'Leather', 'L'],
                       ['B33', 'Nutri-Bullet Blender', 25, 'n', 'y',
                        'Nutri-Bullet', 12]]
        with patch('builtins.input', side_effect=item_inputs[0]):
            main.add_new_item()
        with patch('builtins.input', side_effect=item_inputs[1]):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, compare)
        