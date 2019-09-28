import sys
sys.path.append('inventory_management')
import inventory_management.main as main
import inventory_management.market_prices as mp
from unittest import TestCase
from unittest.mock import MagicMock, patch
from inventory_management.inventory import Inventory
from inventory_management.electric_appliances import ElectricAppliances
from inventory_management.furniture import Furniture

class InventoryTest(TestCase):
    """ Tests for the Inventory Class """

    def test_inventory(self):
        """ Test creation of an Inventory item """

        inventory = Inventory(1, 'Dummy Description', 100, 10)

        self.assertEqual({'product_code': 1,
                          'description': 'Dummy Description',
                          'market_price': 100,
                          'rental_price': 10}, inventory.return_as_dictionary())

class ElectricAppliancesTest(TestCase):
    """ Tests for the ElectricAppliances Class """

    def test_electricappliances(self):
        """ Test creation of an ElectriAppliances item """

        electric_appliance = ElectricAppliances(2, 'Dummy Description', 100, 10, 'Samsung', 120)

        self.assertEqual({'product_code': 2,
                          'description': 'Dummy Description',
                          'market_price': 100,
                          'rental_price': 10,
                          'brand': 'Samsung',
                          'voltage': 120}, electric_appliance.return_as_dictionary())

class FurnitureTest(TestCase):
    """ Tests for the Furniture Class """

    def test_furniture(self):
        """ Test creation of a Furniture item """

        furniture = Furniture(3, 'Dummy Description', 100, 10, 'Upholstery', 'L')

        self.assertEqual({'product_code': 3,
                          'description': 'Dummy Description',
                          'market_price': 100,
                          'rental_price': 10,
                          'material': 'Upholstery',
                          'size': 'L'}, furniture.return_as_dictionary())

class MainTest(TestCase):
    """ Tests the Main units """

    def test_main_menu(self):
        """ Test the main menu function """

        with patch('builtins.input', side_effect="1"):
            self.assertEqual(main.main_menu().__name__, "add_new_item")

        with patch('builtins.input', side_effect="2"):
            self.assertEqual(main.main_menu().__name__, "item_info")

        with patch('builtins.input', side_effect="q"):
            self.assertEqual(main.main_menu().__name__, "exit_program")

    def test_get_price(self):
        """ Test the get_price function """
        main.get_price = MagicMock(return_value=75)
        self.assertEqual(main.get_price("100"), 75)

    def test_add_new_item(self):
        """ Test the add_new_item function """

        main.full_inventory = {}
        inventory = {'product_code': 1,
                     'description': 'Dummy Description',
                     'market_price': 24,
                     'rental_price': 10}
        furniture = {'product_code': 2,
                     'description': 'Dummy Description',
                     'market_price': 24,
                     'rental_price': 10,
                     'material': 'Upholstery',
                     'size': 'L'}
        electric_appliance = {'product_code': 3,
                              'description': 'Dummy Description',
                              'market_price': 24,
                              'rental_price': 10,
                              'brand': 'Samsung',
                              'voltage': 120}

        # Test adding regular inventory item
        input = [1, 'Dummy Description', 10, 'n', 'n']
        with patch('builtins.input', side_effect=input):
            main.add_new_item()
            self.assertEqual(main.full_inventory[1], inventory)

        # Test adding furniture item
        input = [2, 'Dummy Description', 10, 'y', 'Upholstery', 'L']
        with patch('builtins.input', side_effect=input):
            main.add_new_item()
            self.assertEqual(main.full_inventory[2], furniture)

        # Test adding electic appliance  item
        input = [3, 'Dummy Description', 10, 'n', 'y', 'Samsung', 120]
        with patch('builtins.input', side_effect=input):
            main.add_new_item()
            self.assertEqual(main.full_inventory[3], electric_appliance)

    def test_item_info(self):
        """ Test the item_info function """

        # Test valid inventory
        main.full_inventory[1] = {'product_code': 1,
                                  'description': 'Dummy Description',
                                  'market_price': 24,
                                  'rental_price': 10}
        test_output = ('product_code:1\n'
                       'description:Dummy Description\n'
                       'market_price:24\n'
                       'rental_price:10\n')
        with patch('builtins.input', side_effect=[1]):
            self.assertEqual(main.item_info(), print(test_output))

        # Test missing inventory
        with patch('builtins.input', side_effect=[2]):
            self.assertEqual(main.item_info(), print("Item not found in inventory"))


    def test_exit_program(self):
        """ Test the exit_program function """

        with self.assertRaises(SystemExit):
            main.exit_program()
