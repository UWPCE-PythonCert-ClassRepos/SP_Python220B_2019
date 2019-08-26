# test_unit.py
"""Create unit tests for inventory management classes."""
import unittest
from unittest import mock

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.market_prices import get_latest_price
from inventory_management import main
from inventory_management.main import FULL_INVENTORY


class InventoryTests(unittest.TestCase):
    """Inventory class tests."""
    def setUp(self):
        self.item = Inventory('1025', "test item", '80.00', '10.00')

    def test_init(self):
        # test inventory item initializes and correct sets initial attributes/properties
        self.assertEqual(self.item.product_code, '1025')
        self.assertEqual(self.item.description, "test item")
        self.assertEqual(self.item.market_price, '80.00')
        self.assertEqual(self.item._rental_price, '10.00')

    def test_dict_return(self):
        # test that a dictionary of the item is returned and the fields are correct
        inven_dict = self.item.return_as_dictionary()
        self.assertIsInstance(inven_dict, dict, "testing output is of type dictionary")
        self.assertEqual(inven_dict["product_code"], '1025')
        self.assertEqual(inven_dict["description"], "test item")
        self.assertEqual(inven_dict["market_price"], '80.00')
        self.assertEqual(inven_dict["rental_price"], '10.00')


class FurnitureTests(unittest.TestCase):
    """Contains all the tests for the Furniture Class."""
    def setUp(self):
        self.chair = Furniture('100', "this is a chair", '150.00', '5.00')
        self.chair2 = Furniture('120', "this is chair #2", '180.00', '0.00', material="Leather",
                                size="small")

    def test_init(self):
        """Test we can initialize a piece of Furniture properly."""
        # test chair with no material or size
        self.assertEqual(self.chair.size, "N/A")
        self.assertEqual(self.chair.material, "N/A")

        # test chair with material and size defined
        self.assertEqual(self.chair2.size, "small")
        self.assertEqual(self.chair2.material, "Leather")

    def test_return_as_dict(self):
        """Test dictionary function for extended furniture needs."""
        chair2_dict = self.chair2.return_as_dictionary()

        self.assertIsInstance(chair2_dict, dict)
        self.assertEqual(chair2_dict["size"], "small")
        self.assertEqual(chair2_dict["material"], "Leather")


class ElectricAppliancesTests(unittest.TestCase):
    """ElectricAppliances class tests."""
    def setUp(self):
        self.toaster = ElectricAppliances('526', "toaster", '50.00', '23.26')
        self.fridge = ElectricAppliances('9610', "fridge", '850.00', '150.00', voltage='120',
                                         brand="whirlpool")

    def test_init(self):
        self.assertEqual(self.toaster.brand, "N/A")
        self.assertEqual(self.toaster.voltage, "N/A")

        self.assertEqual(self.fridge.voltage, '120')
        self.assertEqual(self.fridge.brand, "whirlpool")

    def test_return_as_dict(self):
       fridge_dict = self.fridge.return_as_dictionary()
       self.assertEqual(fridge_dict["brand"], "whirlpool")
       self.assertEqual(fridge_dict["voltage"], '120')


class MarketPriceTest(unittest.TestCase):
    """Market price module tests."""
    def test_market_prices(self):
        self.assertEqual(get_latest_price(), 24)


class MainTests(unittest.TestCase):
    """Main module tests."""

    def test_main_menu(self):
        """Test main menu returns the proper function call."""
        with mock.patch('builtins.input', side_effect=['1', '2', 'q']):
            self.assertEqual(main.main_menu(), main.add_new_item)
            self.assertEqual(main.main_menu(), main.item_info)
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_get_price(self):
        main.get_price()

    def test_add_new_item(self):
        # test adding regular item
        reg_item = ['10', 'reg_item', '10.00', 'n', 'n']
        comp_dict = {'10': {'product_code': '10',
                                'description': 'reg_item',
                                'market_price': 24,
                                'rental_price': '10.00'}}

        with mock.patch('builtins.input', side_effect=reg_item):
            main.add_new_item()

        self.assertEqual(FULL_INVENTORY, comp_dict)

        # test adding electrical appliance
        electrical_item = ['50', 'elec_item', '30.00', 'n', 'y', 'LG', '240']
        comp_dict['50'] = {'product_code': '50',
                           'description': 'elec_item',
                           'market_price': 24,
                           'rental_price': '30.00',
                           'brand': 'LG',
                           'voltage': '240'}

        with mock.patch('builtins.input', side_effect=electrical_item):
            main.add_new_item()

        self.assertEqual(FULL_INVENTORY, comp_dict)

        # test adding furniture
        furniture_item = ['100', 'furn_item', '5.00', 'y', 'cloth', 'm']
        comp_dict['100'] = {'product_code': '100',
                            'description': 'furn_item',
                            'market_price': 24,
                            'rental_price': '5.00',
                            'material': 'cloth',
                            'size': 'm'}

        with mock.patch('builtins.input', side_effect=furniture_item):
            main.add_new_item()

        self.assertEqual(FULL_INVENTORY, comp_dict)

    def test_item_info(self):
        reg_item = ['10', 'reg_item', '10.00', 'n', 'n']

        with mock.patch('builtins.input', side_effect=reg_item):
            main.add_new_item()

        with mock.patch('builtins.input', side_effect=['10']):
            main.item_info()

        with mock.patch('builtins.input', side_effects=['0001']):
            main.item_info()

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()