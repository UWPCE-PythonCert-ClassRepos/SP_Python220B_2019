from unittest import TestCase
import unittest
import sys
from inventory_management.main import main_menu
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances

from unittest.mock import patch


class ModuleTests(TestCase):
    def test_module(self):
        inventory_item = Inventory(1, 'pan', 50, 10)
        electric_item = ElectricAppliances(2, 'computer', 50, 10, 'Delly', 5)
        furniture_item = Furniture(3, 'bed', 50, 10, 'wood', 'queen')

        inventory_item_info = inventory_item.return_as_dictionary()
        electric_item_info = electric_item.return_as_dictionary()
        furniture_item_info = furniture_item.return_as_dictionary()

        self.assertEqual(1, inventory_item_info['productCode'])
        self.assertEqual('pan', inventory_item_info['description'])
        self.assertEqual(2, electric_item_info['productCode'])
        self.assertEqual('computer', electric_item_info['description'])
        self.assertEqual(3, furniture_item_info['productCode'])
