# -*- coding: utf-8 -*-
"""
Created on Sun Jun 9 10:34:37 2019
@author: Florentin Popescu
"""
#======================================
# imports
import unittest
from unittest import TestCase

from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliances import Electric

#======================================
class ModuleTests(TestCase):
    """ module test """
    def test_module(self):
        """ initiate item's attributes and test """
        inventory_item = Inventory(1, 'stapler', 10, 5)
        furniture_item = Furniture(2, 'sofa', 20, 10, 'wood', 'king')
        electric_item = Electric(3, 'boiler', 30, 15, '', 8)

        inventory_item_info = inventory_item.return_as_dictionary()
        furniture_item_info = furniture_item.return_as_dictionary()
        electric_item_info = electric_item.return_as_dictionary()

        self.assertEqual(1, inventory_item_info['product_code'])
        self.assertEqual('stapler', inventory_item_info['description'])

        self.assertEqual(2, furniture_item_info['product_code'])
        self.assertEqual('sofa', furniture_item_info['description'])

        self.assertEqual(3, electric_item_info['product_code'])
        self.assertEqual('boiler', electric_item_info['description'])

#======================================
if __name__ == "__main__":
    unittest.main()

#============= END ====================
#======================================
