# Advanced Programming in Python -- Lesson 1 Assignment One
# Jason Virtue
# Start Date 2/1/2020

"""
Integration Tests for inventory_management modules
"""

import unittest
from unittest import TestCase
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances

#======================================
class ModuleTests(TestCase):
    """ module test """
    def test_module(self):
        """ Test out inventory items """
        inventory_item = Inventory(1, 'stapler', 10, 5)
        furniture_item = Furniture(2, 'sofa', 20, 10, 'wood', 'king')
        electric_item = ElectricAppliances(3, 'boiler', 30, 15, '', 8)

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