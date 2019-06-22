"""
Created by Randi Peterson 6/15/2019
Edited by R. Peterson 6/22/2019
"""

"""This file conducts unit testing for the Norton code"""
from unittest import TestCase
import sys
sys.path.append('inventory_management')
from inventory_class import Inventory
from furniture_class import Furniture
from electric_appliances_class import ElectricAppliances
from market_prices import get_latest_price
from main import FULL_INVENTORY, main_menu, get_price, add_new_item, item_info, exit_program
from unittest.mock import MagicMock, patch


class InventoryTests(TestCase):
    """Tests for the Inventory object"""

    def setUp(self):
        """Gives set up parameters"""
        self.product_code = '26'
        self.description = 'couch'
        self.market_price = "$50"
        self.rental_price = "$20"
        self.test_inventory = Inventory(self.product_code, self.description, self.market_price,
                                    self.rental_price)
        self.expected_dict = {'product_code': self.product_code, 'description': self.description,
                         'market_price': self.market_price, 'rental_price': self.rental_price}

    def test_inventory_creation(self):
        """Tests successful creation of inventory object"""
        assert self.test_inventory.product_code == self.product_code
        assert self.test_inventory.description == self.description
        assert self.test_inventory.market_price == self.market_price
        assert self.test_inventory.rental_price == self.rental_price

    def test_dict_creation(self):
        """Tests dict creation and accuracy"""
        test_out_dict = self.test_inventory.return_as_dictionary()
        assert test_out_dict == self.expected_dict


class ElectricApplianceTests(TestCase):
    """Tests the Electrical Appliance Subclass of Inventory"""

    def setUp(self):
        """Sets up the initial paramaeters"""
        self.product_code = '26'
        self.description = 'Oven'
        self.market_price = '$50'
        self.rental_price = '$20'
        self.brand = 'Bosch'
        self.voltage = '120V'

        self.test_appliance = ElectricAppliances(self.product_code, self.description,
                                                 self.market_price, self.rental_price, self.brand,
                                                 self.voltage)
        self.expected_appliance_dict = {'product_code': self.product_code,
                                        'description': self.description,
                                        'market_price': self.market_price,
                                        'rental_price': self.rental_price,
                                        'brand': self.brand, 'voltage': self.voltage}

    def test_appliance_creation(self):
        """Tests creation of appliance subclass"""
        assert self.test_appliance.product_code == self.product_code
        assert self.test_appliance.description == self.description
        assert self.test_appliance.market_price == self.market_price
        assert self.test_appliance.rental_price == self.rental_price
        assert self.test_appliance.brand == self.brand
        assert self.test_appliance.voltage == self.voltage

    def test_appliance_dict(self):
        """Tests successful creation of the dictionary"""
        test_app_dict = self.test_appliance.return_as_dictionary()
        assert test_app_dict == self.expected_appliance_dict

class FurnitureTests(TestCase):
    """Tests creation of furniture subclass"""
    def setUp(self):
        """Sets up the initial paramaeters"""
        self.product_code = '26'
        self.description = 'Oven'
        self.market_price = '$50'
        self.rental_price = '$20'
        self.material = 'Leather'
        self.size = 'M'

        self.test_furniture = Furniture(self.product_code, self.description,
                                                 self.market_price, self.rental_price,
                                                 self.material, self.size)
        self.expected_furniture_dict = {'product_code': self.product_code,
                                        'description': self.description,
                                        'market_price': self.market_price,
                                        'rental_price': self.rental_price,
                                        'material': self.material, 'size': self.size}

    def test_furniture_creation(self):
        """Tests creation of furniture subclass"""
        assert self.test_furniture.product_code == self.product_code
        assert self.test_furniture.description == self.description
        assert self.test_furniture.market_price == self.market_price
        assert self.test_furniture.rental_price == self.rental_price
        assert self.test_furniture.material == self.material
        assert self.test_furniture.size == self.size

    def test_appliance_dict(self):
        """Tests successful creation of the dictionary"""
        test_app_dict = self.test_furniture.return_as_dictionary()
        assert test_app_dict == self.expected_furniture_dict

class MainTests(TestCase):
    """Tests the main.py module and its functions"""

    def test_add_new_item(self):
        """Tests adding new input of furniture, appliance, and other"""

        furniture_input = ('01', 'Couch', 100, 'y', 'leather', 'M')
        comparison_furniture = {'01': {'product_code': '01', 'description': 'Couch',
                                       'market_price': 24, 'material': 'leather',
                                       'rental_price': 100, 'size': 'M'}}

        with patch('builtins.input', side_effect = furniture_input):
            add_new_item()
        self.assertEqual(FULL_INVENTORY, comparison_furniture)

        electrical_input = ('154', 'Stove', 150, 'n', 'y', 'Bosch', 120)
        comparison_inventory = {'01': {'product_code': '01', 'description': 'Couch',
                                       'market_price': 24, 'material': 'leather',
                                       'rental_price': 100, 'size': 'M'},
                                '154': {'product_code': '154', 'description': 'Stove',
                                        'market_price': 24, 'rental_price': 150,
                                        'brand': 'Bosch', 'voltage': 120}}

        with patch('builtins.input', side_effect = electrical_input):
            add_new_item()
        self.assertEqual(FULL_INVENTORY, comparison_inventory)

        other_input = ('666', 'Potato', 10, 'n', 'n')
        final_comparison_inventory = {'01': {'product_code': '01', 'description': 'Couch',
                                             'market_price': 24, 'material': 'leather',
                                             'rental_price': 100, 'size': 'M'},
                                      '154': {'product_code': '154', 'description': 'Stove',
                                              'market_price': 24, 'rental_price': 150,
                                              'brand': 'Bosch', 'voltage': 120},
                                      '666': {'product_code': '666', 'description': 'Potato',
                                              'market_price': 24, 'rental_price': 10}}

        with patch('builtins.input', side_effect = other_input):
            add_new_item()
        self.assertEqual(FULL_INVENTORY, final_comparison_inventory)

    def test_item_info(self):
        """Tests item info"""
        furniture_input = ('01', 'Couch', 100, 'y', 'leather', 'M')
        with patch('builtins.input', side_effect=furniture_input):
            add_new_item()

        with patch('builtins.input', side_effect = ['01']):
            self.assertEqual(item_info(), None)

        with patch('builtins.input', side_effect = ['02']):
            self.assertEqual(item_info(), None)

    def test_exit_program(self):
        """Tests exit program causes system exit"""
        with self.assertRaises(SystemExit):
            exit_program()

    def test_main_menu_add(self):
        """Tests add_new_item call from main menu"""
        with patch('builtins.input', side_effect=['hi','1']):
            self.assertEqual(main_menu(), add_new_item)

    def test_main_menu_info(self):
        """Tests item_info call from main menu"""
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main_menu(), item_info)

    def test_pass_main_menu_exit(self):
        """Tests exit call from main menu"""
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main_menu(), exit_program)

    def test_get_price(self):
        """Tests get price is calling correctly"""
        self.get_price = MagicMock(return_value=24)
       # self.assertEqual(24, get_price())

class MarketPriceTests(TestCase):
    """Tests the market_price function, even though we cannot adjust it"""

    def test_get_latest_price(self):
        """Tests that the function returns the expected value hardcoded"""
        self.assertEqual(get_latest_price(),24)
