from unittest import TestCase
from unittest.mock import MagicMock

import sys
sys.path.append('./inventory_management')
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture

class InventoryTests(TestCase):

    def test_inventory(self):
        test_inv = Inventory(1234, "test product", 567, 246)    
        self.assertIsInstance(test_inv, Inventory)
        test_dict = {"product_code": 1234, "description": "test product",
                     "market_price": 567, "rental_price": 246}
        self.assertDictEqual(test_dict, test_inv.return_as_dictionary())
        
class ElectricAppliancesTest(TestCase):
    
    def test_electric_inventory(self):
        test_elect_inv = ElectricAppliances(1234, "test product", 567, 246, "My Brand", 440)    
        self.assertIsInstance(test_elect_inv, ElectricAppliances)
        test_elect_dict = {"product_code": 1234, "description": "test product",
                     "market_price": 567, "rental_price": 246, "brand": "My Brand",
                     "voltage": 440}
        self.assertDictEqual(test_elect_dict, test_elect_inv.return_as_dictionary())
        
class FurnitureTest(TestCase):
    
    def test_furniture(self):
        test_furn = Furniture(1234, "test product", 567, 246, "wood", "L")    
        self.assertIsInstance(test_furn, Furniture)
        test_furn_dict = {"product_code": 1234, "description": "test product",
                     "market_price": 567, "rental_price": 246, "material": "wood",
                     "size": "L"}
        self.assertDictEqual(test_furn_dict, test_furn.return_as_dictionary())





