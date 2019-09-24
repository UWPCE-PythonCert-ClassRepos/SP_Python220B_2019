'''unit testing individual components of inventory management'''
import sys
sys.path.append("./inventory_management")
from unittest import TestCase
from unittest.mock import patch
from io import StringIO
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.market_prices import get_latest_price
import inventory_management.main as main


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
        furniture = Furniture('DINE_TBL', 'Dining Table', 500, 50, 'wood', 'L')
        output = furniture.return_as_dictionary()
        self.assertEqual(output['material'], 'wood')
        self.assertEqual(output['size'], 'L')

class MarketPrices(TestCase):
    '''test market price module'''

    def test_market_price(self):
        self.assertEqual(get_latest_price('test'), 24)

class Main(TestCase):

    def test_main_menu(self):
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu().__name__, 'add_new_item')

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu().__name__, 'item_info')

        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu().__name__, 'exit_program')

    def test_get_price(self):
        self.assertEqual(main.get_price('test'), 24)

    def test_add_item(self):
        '''test add generic item'''
        main.FULL_INVENTORY = {}
        new_item = ['1', 'Sectional', 100, 'n', 'n']
        test_add = {'1': {'product_code':'1', 'description': 'Sectional',
                          'market_price': 24, 'rental_price': 100}}

        with patch('builtins.input', side_effect=new_item):
            main.add_new_item()
            self.assertEqual(test_add, main.FULL_INVENTORY)

    def test_add_electric_item(self):
        main.FULL_INVENTORY = {}
        new_e_item = ['MICWV', 'Microwave', 10, 'n', 'y', 'Whirlpool', '1000V']
        test_e_add = {'MICWV': {'product_code': 'MICWV', 'description': 'Microwave',
                                'market_price': 24, 'rental_price': 10,
                                'brand': 'Whirlpool', 'voltage': '1000V'}}

        with patch('builtins.input', side_effect=new_e_item):
            main.add_new_item()
            self.assertEqual(test_e_add, main.FULL_INVENTORY)

    def test_add_furniture_item(self):
        main.FULL_INVENTORY = {}
        new_f_item = ['DINE_TBL', 'Dining Table', 50, 'y', 'wood', 'L']
        test_f_add = {'DINE_TBL': {'product_code': 'DINE_TBL', 'description': 'Dining Table',
                                   'market_price': 24, 'rental_price': 50,
                                   'material': 'wood', 'size': 'L'}}

        with patch('builtins.input', side_effect=new_f_item):
            main.add_new_item()
            self.assertEqual(test_f_add, main.FULL_INVENTORY)

    def test_item_info(self):
        main.FULL_INVENTORY = {'SOFA': {'product_code':'SOFA', 'description': 'Sectional',
                                        'market_price': 24, 'rental_price': 100}}
        inventory = 'product_code:SOFA\ndescription:Sectional\nmarket_price:24\nrental_price:100\n'

        with patch('builtins.input', side_effect=['SOFA']):
            with patch('sys.stdout', new=StringIO()) as result:
                main.item_info()
                self.assertEqual(result.getvalue(), inventory)

        with patch('builtins.input', side_effect='test_fail'):
            with patch('sys.stdout', new=StringIO()) as result:
                main.item_info()
                self.assertEqual(result.getvalue(), 'Item not found in inventory\n')
