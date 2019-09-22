'''unit testing individual components of inventory management'''

from unittest import TestCase
#from unittest.mock import MagicMock
#import io
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
#from inventory_management.market_prices import get_latest_price
#from inventory_management.main import *


class InventoryTests(TestCase):
    '''test inventory module'''

    def test_inventory(self):
        '''tests inventory'''
        inventory = Inventory('SOFA', 'Black sectional', 1000, 100)
        self.assertEqual(inventory.return_as_dictionary(),
                         {'product_code': 'SOFA', 'description': 'Black sectional',
                          'market_price': 1000, 'rental_price': 100})


class ElectricAppliancesTests(TestCase):
    '''test electrical appliances module'''

    def test_electrical_appliances(self):
        '''tests electronics'''
        elec_app = ElectricAppliances('MICWV', 'Microwave', 100, 10, 'Whirlpool', '1000V')
        output = elec_app.return_as_dictionary()
        self.assertEqual(output['brand'], 'Whirlpool')
        self.assertEqual(output['voltage'], '1000V')


class FurnitureTests(TestCase):
    '''test furniture module'''

    def test_furniture(self):
        '''tests furniture class'''
        furniture = Furniture('DINE_TBL', 'Dining Table', 500, 50, 'wood', '72in x 48in')
        output = furniture.return_as_dictionary()
        self.assertEqual(output['material'], 'wood')
        self.assertEqual(output['size'], '72in x 48in')

class MarketPrices(TestCase):
    '''test market price module'''

    def test_market_price(self):
        pass

class Main(TestCase):
    pass
