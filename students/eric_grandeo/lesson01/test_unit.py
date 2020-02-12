from unittest import TestCase
from unittest.mock import MagicMock

from inventory_management.inventory_class import Inventory

class InventoryTests(TestCase):

    def test_inventory(self):
        test_inv = Inventory(1234, "test product", 567, 246)    
        self.assertIsInstance(test_inv, Inventory)
        test_dict = {"product_code": 1234, "description": "test product",
                     "market_price": 567, "rental_price": 246}
        self.assertEqual(test_dict, test_inv.return_as_dictionary())
        
class ElectricAppliancesTest(TestCase):
    
    pass    


