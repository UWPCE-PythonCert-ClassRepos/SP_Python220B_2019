"""Unit testing for inventory management system"""

from inventory_management.product_classes import Inventory, Furniture, ElectricAppliances
import inventory_management.main as menu
from unittest import TestCase
from unittest.mock import MagicMock


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
                    'description': 'Test Item',
                    'market_price': 50,
                    'rental_price': 80}
        self.assertEqual(inv_dict, test_dict)

class ElectricAppliancesTests(TestCase):
    """ Test for ElectricApplicances class"""
    
    def test_elec_init(self):
        elec = ElectricAppliances(54, 'Test Elec', 200, 300, 'John Deere', 2)
        self.assertEqual(elec.brand, 'John Deere')
        self.assertEqual(elec.voltage, 2)  

    def test_return_dict(self):
        elec = ElectricAppliances(54, 'Test Elec', 200, 300, 'John Deere', 2)
        elec_dict = elec.return_as_dictionary()
        test_dict = {'product_code': 54,
                    'description': 'Test Elec',
                    'market_price': 200,
                    'rental_price': 300,
                    'brand': 'John Deere',
                    'voltage': 2}
        self.assertEqual(elec_dict, test_dict)
    
class FurnitureTests(TestCase):
    """ Test for Furniture class"""

    def test_elec_init(self):
        furn = Furniture(54, 'Test Elec', 200, 300, 'leather', 10)
        self.assertEqual(furn.material, 'leather')
        self.assertEqual(furn.size, 10)

    def test_return_dict(self):
        furn = Furniture(54, 'Test Elec', 200, 300, 'leather', 10)
        furn_dict = furn.return_as_dictionary()
        test_dict = {'product_code': 54,
                    'description': 'Test Elec',
                    'market_price': 200,
                    'rental_price': 300,
                    'material': 'leather',
                    'size': 10}
        self.assertEqual(furn_dict, test_dict)
    
class MainTests(TestCase):
    """ Tests for functions in main """

    def test_main_menu(self):
        """ Tests main menu functionality """

        self.assertEqual(menu.main_menu('1'),menu.add_new_item)
        self.assertEqual(menu.main_menu('2'),menu.item_info)
        self.assertEqual(menu.main_menu('q'),menu.exit_program)

    def test_add_new_item(self):
        """ Tests add item function """

        menu.add_new_item = MagicMock(
            item_code = 44, item_description = 'Test description',
            item_rental_price = 50, item_price = 1000,
            item_material = 'leather', item_size = 'Large',
            item_brand = 'JD', item_voltage = 200,
            is_furniture = 'Y')

        # Test for furniture call -- PROBLEMS HERE
        menu.add_new_item.assert_called_with(44, 'Test description', 
        1000, 50, 'leather', 'Large')

    def test_item_info(self):
        """ Tests item info function """

        # Test case: item code not in full inventory -- HOW TO GET AT IF STATEMENT
        FULL_INVENTORY = [40,50]
        menu.item_info = MagicMock(item_code = 56)
        self.assertEqual(menu.item_info(), "Item not found in inventory")

        

    
    def test_exit(self):
        """ Tests system exit """

        with self.assertRaises(SystemExit):
            menu.exit_program()
    



