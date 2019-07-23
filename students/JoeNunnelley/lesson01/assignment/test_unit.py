#! /usr/bin/env python3
""" The Inventory Management Unit Test Suite """

import io
#import sys
#sys.path.append('./inventory_management')
from unittest import TestCase
from unittest.mock import patch
from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliances import ElectricAppliances
import inventory_management.main as main
import inventory_management.market_prices as market_prices

# Tests for market_prices
class TestMarketPrices(TestCase):
    """ Class for testing the market prices module """
    @classmethod
    def test_market_prices(cls):
        """ Ensure that you get the preset value returned """
        latest_price = market_prices.get_latest_price('CORN')
        assert latest_price == 24


# Tests for inventory module
# InventoryItem class
class TestInventoryClass(TestCase):
    """ Class for testing the inventory class """
    @classmethod
    def test_create_inventory_item(cls):
        """ Create an inventory object and make sure it initializes properly """
        inventory = Inventory('CORN', 'The plant corn', 30, 0)
        item_dict = inventory.return_as_dictionary()
        assert item_dict['productCode'] == 'CORN'
        assert item_dict['description'] == 'The plant corn'
        assert item_dict['marketPrice'] == 30
        assert item_dict['rentalPrice'] == 0


# Tests for furniture module
class TestFurnitureClass(TestCase):
    """ Class for testing the furniture objec type """
    @classmethod
    def test_create_furniture_item(cls):
        """ Create a furniture object and make sure it initializes correctly """
        furniture = Furniture('SOFA', 'A place to sit', 300, 50, 'Cloth', '2 Meters')
        item_dict = furniture.return_as_dictionary()
        assert item_dict['productCode'] == 'SOFA'
        assert item_dict['description'] == 'A place to sit'
        assert item_dict['marketPrice'] == 300
        assert item_dict['rentalPrice'] == 50
        assert item_dict['Material'] == 'Cloth'
        assert item_dict['Size'] == '2 Meters'


# Tests for electric appliances module
class TestElectricalApplianceClass(TestCase):
    """ Class for testing the Electrical Appliance object """
    @classmethod
    def test_create_electrical_appliance_item(cls):
        """ Create an electrical appliance instance and make sure it is initialized correctly """
        appliance = ElectricAppliances('VCR', 'What you walch Betamax on', 3, 0, 'Panasonic', 120)
        item_dict = appliance.return_as_dictionary()
        assert item_dict['productCode'] == 'VCR'
        assert item_dict['description'] == 'What you walch Betamax on'
        assert item_dict['marketPrice'] == 3
        assert item_dict['rentalPrice'] == 0
        assert item_dict['Brand'] == 'Panasonic'
        assert item_dict['Voltage'] == 120


# Tests for main
class TestMainClass(TestCase):
    """ Class for testing the main interface """
    def run_input_test(self, selected, expected_out):
        """ Helper class for validating input selections """
        with patch('builtins.input', side_effect=selected):
            self.assertEqual(main.main_menu().__name__, expected_out)


    def test_main_valid_prompts(self):
        """ Test to make sure that valid inputs are handled properly """
        self.run_input_test('1', 'add_new_item')
        self.run_input_test('2', 'item_info')
        self.run_input_test('q', 'exit_program')


    def test_main_invalid_prompts(self):
        """ Test to ensure that invalid inputs are handled properly """
        with self.assertRaises(StopIteration):
            self.run_input_test('3', '')


    @classmethod
    def test_get_price(cls):
        """
        Test to ensure that on a given inventory set, get_price will return
        the correct value.  This patches get_latest_prices since the method
        implementation is not functional
        """
        main.FULL_INVENTORY = {'CORN': {'product_code': 'CORN',
                                        'description': 'This is corn',
                                        'market_price': 24,
                                        'rental_price': 50},
                               'WATER': {'product_code': 'WATER',
                                         'description': 'This is water',
                                         'market_price': 40,
                                         'rental_price': 0,}}

        assert main.get_price('CORN') == 24

        with patch('market_prices.get_latest_price', return_value=50):
            assert main.get_price('WHEAT') == 50


    def test_exit_program(self):
        """
        Test to validate that the correct signal is
        raised when exit_program is called.
        """
        with self.assertRaises(SystemExit):
            main.exit_program()


    @classmethod
    def test_item_add_furniture(cls):
        """ Test to validate the addition of a furniture entry to the inventory """
        main.FULL_INVENTORY = {}
        user_inputs = ['CHAIR', 'This is a chair', 30, 'Y', 'wood', 'L']
        with patch('builtins.input', side_effect=user_inputs):
            main.add_new_item()
            assert main.FULL_INVENTORY.keys()
            assert 'CHAIR' in main.FULL_INVENTORY.keys()


    @classmethod
    def test_item_add_electrical_appliance(cls):
        """
        Test to validate the addition of a electrical appliance entry
        to the inventory
        """
        main.FULL_INVENTORY = {}
        user_inputs = ['TV', 'This is a tv', 300, 'N', 'Y', 'metal', 'S']
        with patch('builtins.input', side_effect=user_inputs):
            main.add_new_item()
            assert main.FULL_INVENTORY.keys()
            assert 'TV' in main.FULL_INVENTORY.keys()


    @classmethod
    def test_item_add_standard(cls):
        """ Test to validate the addition of a standard entry to the inventory """
        main.FULL_INVENTORY = {}
        user_inputs = ['CORN', 'This is corn', 30, 'N', 'n']
        with patch('builtins.input', side_effect=user_inputs):
            main.add_new_item()
            assert main.FULL_INVENTORY.keys()
            assert 'CORN' in main.FULL_INVENTORY.keys()


    @classmethod
    def test_item_info_found(cls):
        """
        Test to validate that an item can be found when it exists
        in the inventory
        """
        main.FULL_INVENTORY = {'CORN': {'product_code': 'CORN',
                                        'description': 'This is corn',
                                        'market_price': 24,
                                        'rental_price': 50},
                               'WATER': {'product_code': 'WATER',
                                         'description': 'This is water',
                                         'market_price': 40,
                                         'rental_price': 0,}}

        with patch('builtins.input', side_effect='CORN'):
            with patch('sys.stdout', new=io.StringIO()) as actual_result:
                main.item_info()
                expected_result_strings = ["productCode:CORN",
                                           "description:This is corn",
                                           "marketPrice:24",
                                           "rentalPrice:50"]
                for expected in expected_result_strings:
                    assert actual_result.getvalue().find(expected)


    @classmethod
    def test_item_info_not_found(cls):
        """
        Test to validate that an item not found when it doesn't exist
        in the inventory returns the correct message
        """
        main.FULL_INVENTORY = {'CORN': {'product_code': 'CORN',
                                        'description': 'This is corn',
                                        'market_price': 24,
                                        'rental_price': 50},
                               'WATER': {'product_code': 'WATER',
                                         'description': 'This is water',
                                         'market_price': 40,
                                         'rental_price': 0,}}

        with patch('builtins.input', side_effect='WHEAT'):
            with patch('sys.stdout', new=io.StringIO()) as actual_result:
                main.item_info()
                expected_result_string = ["Item not found in inventory"]
                for expected in expected_result_string:
                    assert not actual_result.getvalue().find(expected)
