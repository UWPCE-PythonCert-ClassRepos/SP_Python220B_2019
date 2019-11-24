from inventory_management.product_classes import Inventory, Furniture, ElectricAppliances
import inventory_management.main
from unittest import TestCase 

class InventoryTests(TestCase):
    """Test for the Inventory class"""

    def test_inv_init(self):
        inv = Inventory(125, 'Test Item', 50, 80)
        self.assertEqual(inv.product_code, 125)
        self.assertEqual(inv.description, 'Test Item')
        self.assertEqual(inv.market_price, 50)
        self.assertEqual(inv.rental_price, 80)  

    def test_return_dict(self):
        inv = Inventory(125, 'Test Item', 50, 80)
        inv_dict = inv.return_as_dictionary()
        test_dict = {'product_code': 125,
                    'description': 'Test item',
                    'market_price': 50,
                    'rental_price': 80}
        self.assertEqual(inv_dict, test_dict)

class ElectricAppliancesTests(TestCase):
    """ Test for ElectricApplicances class"""
    
    