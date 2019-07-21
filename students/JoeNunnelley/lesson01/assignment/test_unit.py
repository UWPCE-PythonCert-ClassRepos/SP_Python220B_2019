#! /usr/bin/env python3

from unittest import TestCase
#from unittest.mock import patch

from inventory_management.inventory import Inventory
from inventory_management.furniture import Furniture
from inventory_management.electric_appliances import ElectricAppliances
import inventory_management.main as main
import inventory_management.market_prices as market_prices

# Tests for market_prices
#@patch('market_prices.get_latest_price')



# Tests for inventory module
# InventoryItem class
class TestInventoryClass(TestCase):
    def test_create_inventory_item(self):
        print('Test Inventory: Class Init')
        a = Inventory('CORN', 'The plant corn', 30, 0)
        item_dict = a.return_as_dictionary()
        assert item_dict['productCode'] == 'CORN'
        assert item_dict['description'] == 'The plant corn'
        assert item_dict['marketPrice'] == 30
        assert item_dict['rentalPrice'] == 0


# Tests for furniture module
class TestFurnitureClass(TestCase):
    def test_create_furniture_item(self):
        print('Test Furniture: Class Init')
        a = Furniture('SOFA', 'A place to sit', 300, 50, 'Cloth', '2 Meters')
        item_dict = a.return_as_dictionary()
        assert item_dict['productCode'] == 'SOFA'
        assert item_dict['description'] == 'A place to sit'
        assert item_dict['marketPrice'] == 300
        assert item_dict['rentalPrice'] == 50
        assert item_dict['Material'] == 'Cloth'
        assert item_dict['Size'] == '2 Meters'


# Tests for electric appliances module
class TestElectricalApplianceClass(TestCase):
    def test_create_electrical_appliance_item(self):
        print('Test Electrical Appliance: Class Init')
        a = ElectricAppliances('VCR', 'What you walch Betamax on', 3, 0, 'Panasonic', 120)
        item_dict = a.return_as_dictionary()
        assert item_dict['productCode'] == 'VCR'
        assert item_dict['description'] == 'What you walch Betamax on'
        assert item_dict['marketPrice'] == 3
        assert item_dict['rentalPrice'] == 0
        assert item_dict['Brand'] == 'Panasonic'
        assert item_dict['Voltage'] == 120


# Tests for main
class TestMainClass(TestCase):
    def test_

