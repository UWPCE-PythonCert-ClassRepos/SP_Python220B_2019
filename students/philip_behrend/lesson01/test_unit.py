"""Unit testing for inventory management system"""

from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch
from inventory_management.product_classes import Inventory, Furniture, ElectricAppliances
import inventory_management.main as menu


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
        """ Tests main menu selection functionality """

        self.assertEqual(menu.main_menu('1'),menu.add_new_item)
        self.assertEqual(menu.main_menu('2'),menu.item_info)
        self.assertEqual(menu.main_menu('q'),menu.exit_program)

    def test_add_new_furniture(self):
        """ Tests add item function IF furniture """

        responses = (44, 'Test description', 50, 'y', 'leather', 'L')
        expected_dict = {'product_code': 44, 'description': 'Test description', 
                        'market_price': 24, 'rental_price': 50, 
                        'material': 'leather', 'size': 'L'}
        with patch('builtins.input', side_effect = responses):
            menu.FULL_INVENTORY = {}
            menu.add_new_item()
            self.assertEqual(menu.FULL_INVENTORY[44], expected_dict)

    def test_add_new_electric(self):
        """ Tests add item function IF electrical applicance """

        responses = (22, 'Test description', 50, 'n', 'y', 'John Deere', 200)
        expected_dict = {'product_code': 22, 'description': 'Test description', 
                        'market_price': 24, 'rental_price': 50, 
                        'brand': 'John Deere', 'voltage': 200}
        with patch('builtins.input', side_effect = responses):
            menu.FULL_INVENTORY = {}
            menu.add_new_item()
            self.assertEqual(menu.FULL_INVENTORY[22], expected_dict)

    def test_add_new_other(self):
        """ Tests add item function IF electrical applicance """

        responses = (99, 'Test description', 50, 'n', 'n')
        expected_dict = {'product_code': 99, 'description': 'Test description', 
                        'market_price': 24, 'rental_price': 50}
        with patch('builtins.input', side_effect = responses):
            menu.FULL_INVENTORY = {}
            menu.add_new_item()
            self.assertEqual(menu.FULL_INVENTORY[99], expected_dict)


    def test_item_info_negative(self):
        """ Tests item info function if item code not present """

        menu.input = Mock(return_value = 44)
        FULL_INVENTORY = {'item_code': 99, 'description': 'Test description', 
                        'market_price': 24, 'rental_price': 50}
        self.assertEqual(menu.item_info(),print("Item not found in inventory"))

    def test_item_info_positive(self):
        """ Tests item info function """
        menu.input = Mock(return_value = 99)
        FULL_INVENTORY = {'item_code': 99, 'description': 'Test description', 
                        'market_price': 24, 'rental_price': 50}
        self.assertEqual(menu.item_info(),print(FULL_INVENTORY))
 
    def test_exit(self):
        """ Tests system exit """
        with self.assertRaises(SystemExit):
            menu.exit_program()
    



