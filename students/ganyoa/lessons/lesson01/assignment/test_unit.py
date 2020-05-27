import sys
import io
#sys.path.append('inventory_management')

from unittest import TestCase
from unittest.mock import patch, MagicMock

import inventory_management.main as main
import inventory_management.market_prices as mp
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory

class InventoryTest(TestCase):
    '''unittest the Inventory class under the inventory_class module'''

    def setUp(self):
        '''create an instance from the Inventory class, from inventory_class module'''
        self.inventory = Inventory('product01', 'description01', 999, 555)

    def test_inventory(self):
        '''test each attribute for instance self.inventory'''
        self.assertEqual('product01', self.inventory.product_code)
        self.assertEqual('description01', self.inventory.description)
        self.assertEqual(999, self.inventory.market_price)
        self.assertEqual(555, self.inventory.rental_price)

    def test_inventory_dict(self):
        '''test attributes are stored correctly in the dictionary'''
        self.assertEqual({'product_code': 'product01', 'description': 'description01', 'market_price': 999, 'rental_price': 555},
        self.inventory.return_as_dictionary())

class ElectricAppliancesTest(TestCase):
    '''unittest the ElectricAppliances class under the electric_appliances_class module'''

    def setUp(self):
        '''create an instance from the ElectricAppliances class, from electric_appliances_class module'''
        self.electric_appliances = ElectricAppliances('product02', 'description02', 444, 222, 'brand01', 220)

    def test_electric_appliances(self):
        self.assertEqual('product02', self.electric_appliances.product_code)
        self.assertEqual('description02', self.electric_appliances.description)
        self.assertEqual(444, self.electric_appliances.market_price)
        self.assertEqual(222, self.electric_appliances.rental_price)
        self.assertEqual('brand01', self.electric_appliances.brand)
        self.assertEqual(220, self.electric_appliances.voltage)

    def test_electric_appliances_dict(self):
        self.assertEqual({'product_code': 'product02', 'description': 'description02', 'market_price': 444, 'rental_price': 222, 'brand': 'brand01', 'voltage': 220},
        self.electric_appliances.return_as_dictionary())

class FurnitureTest(TestCase):
    '''unittest the Furniture class under the furniture_class module'''

    def setUp(self):
        '''
        create an instance from the Furniture class,
        from furniture_class module
        '''
        self.furniture = Furniture('product03', 'description03', 555, 111, 'material01', 'M')

    def test_furniture(self):
        self.assertEqual('product03', self.furniture.product_code)
        self.assertEqual('description03', self.furniture.description)
        self.assertEqual(555, self.furniture.market_price)
        self.assertEqual(111, self.furniture.rental_price)
        self.assertEqual('material01', self.furniture.material)
        self.assertEqual('M', self.furniture.size)

    def test_furniture_dict(self):
        self.assertEqual({'product_code': 'product03', 'description': 'description03', 'market_price': 555, 'rental_price': 111, 'material': 'material01', 'size': 'M'},
        self.furniture.return_as_dictionary())

class MarketPriceTest(TestCase):
    '''unittest market_price'''
    def test_market_price(self):
        self.assertEqual(24, mp.get_latest_price('test'))

class MainTest(TestCase):
    '''unittest user input into main_menu'''

    def test_main_menu(self): # Tests main menu setup
        with patch('builtins.input', side_effect='1'): # side_effect is the input value stored
            self.assertIs(main.main_menu(), main.add_new_item)
        with patch('builtins.input', side_effect='2'):
            self.assertIs(main.main_menu(), main.item_info)
        with patch('builtins.input', side_effect='q'):
            self.assertIs(main.main_menu(), main.exit_program)

    def test_add_new_item(self):
        '''test add_new_item function with user entering in furniture, appliance, and other'''
        with patch('builtins.input', side_effect=('furniture01', 'chair', 39, 'y', 'suede', 'L')):
            main.add_new_item()

        with patch('builtins.input', side_effect=('appliance01', 'radio', 15, 'n', 'y', 'top', 120)):
            main.add_new_item()

        with patch('builtins.input', side_effect=('other01', 'misc', 54, 'n', 'n')):
            main.add_new_item()

        self.assertEqual(main.FULL_INVENTORY, {'furniture01': {'product_code': 'furniture01',
                                                   'description': 'chair',
                                                   'market_price': 24,
                                                   'rental_price': 39,
                                                   'material': 'suede',
                                                   'size': 'L'},
                                        'appliance01': {'product_code': 'appliance01',
                                                   'description': 'radio',
                                                   'market_price': 24,
                                                   'rental_price': 15,
                                                   'brand': 'top',
                                                   'voltage': 120},
                                        'other01': {'product_code': 'other01',
                                                   'description': 'misc',
                                                   'market_price': 24,
                                                   'rental_price': 54}})


    def test_item_info(self):
        '''test item_info function if items does and does not exist in FULL_INVENTORY dict'''
        with patch('builtins.input', side_effect = ["nope"]):
            with patch('sys.stdout', new = io.StringIO() ) as input_result:
                main.item_info()
        self.assertEqual(input_result.getvalue(), "Item not found in inventory\n")

        with patch('builtins.input', side_effect = ["appliance01"]):
            with patch('sys.stdout', new = io.StringIO() ) as input_result:
                main.item_info()
        self.assertEqual(input_result.getvalue(), 'product_code:appliance01\n'
                                                  'description:radio\n'
                                                  'market_price:24\n'
                                                  'rental_price:15\n'
                                                  'brand:top\n'
                                                  'voltage:120\n')

    def test_exit_program(self):
        '''confirm if user enters a 'q' the program will exit'''
        with patch('builtins.input', side_effect = ['q']):
            self.assertEqual(main.main_menu(), main.exit_program)