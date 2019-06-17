"""This file conducts unit testing for the Norton code"""
from unittest import TestCase
import sys
sys.path.append('inventory_management')
from inventory_class import Inventory
from furniture_class import Furniture
from electric_appliances_class import ElectricAppliances
from market_prices import get_latest_price
from main import main_menu, get_price, add_new_item, item_info, exit_program

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
    def setUp(self):
        pass

    def test_get_price(self):
        """Tests the print of get price"""
        #This is a useless test but testing print is difficult
        #This makes sure no errors happen
        get_price()

    def test_add_new_item(self):
        pass

    def test_item_info(self):
        pass

    def test_main_menu(self):
        pass

class MarketPriceTests(TestCase):
    """Tests the market_price function, even though we cannot adjust it"""

    def test_get_latest_price(self):
        """Tests that the function returns the expected value hardcoded"""
        assert get_latest_price() == 24
