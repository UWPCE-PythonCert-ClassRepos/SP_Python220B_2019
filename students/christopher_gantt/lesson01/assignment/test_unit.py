'''Unit Testing for Inventory Management System'''
from unittest import TestCase
from unittest.mock import patch

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.market_prices as market_prices
import inventory_management.main as main

class MainTests(TestCase):
    '''tests for main.py module'''
    def test_main_menu(self):
        """tests inputs for main menu"""
        with patch('builtins.input', side_effect='1'):
            function = main.main_menu()
        self.assertEqual(function.__name__, 'add_new_item')

        with patch('builtins.input', side_effect='2'):
            function = main.main_menu()
        self.assertEqual(function.__name__, 'item_info')

        with patch('builtins.input', side_effect='q'):
            function = main.main_menu()
        self.assertEqual(function.__name__, 'exit_program')

    def test_add_new_item(self):
        '''tests adding new items to the inventory'''
        item_one = ['1', 'Painting', '50', 'n', 'n']
        item_two = ['2', 'Desk', '100', 'y', 'wood', 'L']
        item_three = ['3', 'Washer', '200', 'n', 'y', 'Kenmore', '120']
        
        with patch('builtins.input', side_effect = item_one):
            main.add_new_item()

        with patch('builtins.input', side_effect = item_two):
            main.add_new_item()

        with patch('builtins.input', side_effect = item_three):
            main.add_new_item()

        test_dict = {'1':{'product_code': '1',
                          'description': 'Painting',
                          'market_price': 24,
                          'rental_price': '50'},
                     '2':{'product_code': '2',
                          'description': 'Desk',
                          'market_price': 24,
                          'rental_price': '100',
                          'material': 'wood',
                          'size': 'L'},
                     '3':{'product_code': '3',
                          'description': 'Washer',
                          'market_price': 24,
                          'rental_price': '200',
                          'brand': 'Kenmore',
                          'voltage': '120'}}

        self.assertEqual(test_dict, main.return_full_inventory())

    def test_get_price(self):
        '''tests that get_price function will return the price from market prices'''
        assert main.get_price(1) == 24

    def test_item_info(self):
        '''testing to see that the item info function returns the info of a created item'''
        item = ['1', 'desk', '100', 'y', 'wood', 'L' ]
        with patch('builtins.input', side_effect = item):
            main.add_new_item()

        with patch('builtins.input', side_effect = '1'):
            function = main.item_info()
        info = '\n'.join(('product_code:1',
                          'description:desk',
                          'market_price:24',
                          'rental_price:100',
                          'material:wood',
                          'size:L'))
        self.assertEqual(function, info)

    def test_item_info_none(self):
        '''tests item info function when item code is not in the inventory'''
        with patch('builtins.input', side_effect = '4'):
            function = main.item_info()
        self.assertEqual(function, 'Item not found in inventory')    

    def test_exit_program(self):
        '''tests that the exit program function ends the program'''
        with self.assertRaises(SystemExit):
            main.exit_program()


class InventoryClassTests(TestCase):
    '''tests for the inventory class module'''
    def setUp(self):
        '''creates inventory object'''
        self.inventory = Inventory(123, 'inventory description', 23, 5.99)

    def test_inventory_init(self):
        '''tests init values for inventory object'''
        assert self.inventory.product_code == 123
        assert self.inventory.description == 'inventory description'
        assert self.inventory.market_price == 23
        assert self.inventory.rental_price == 5.99

    def test_return_as_dict(self):
        '''tests the return as dict method in class inventory'''
        inventory_dict = self.inventory.return_as_dictionary()
        assert inventory_dict == {'product_code': 123,
                                  'description': 'inventory description',
                                  'market_price': 23,
                                  'rental_price': 5.99}


class FurnitureClassTests(TestCase):
    '''tests for the furniture class module'''
    def setUp(self):
        '''creates a furniture object, a sofa'''
        self.sofa = Furniture(321, 'brown sofa', 300, 100, 'Faux Leather', 'Large')

    def test_init(self):
        '''tests init values for the sofa'''
        assert self.sofa.product_code == 321
        assert self.sofa.description == 'brown sofa'
        assert self.sofa.market_price == 300
        assert self.sofa.rental_price == 100
        assert self.sofa.material == 'Faux Leather'
        assert self.sofa.size == 'Large'

    def test_return_as_dict(self):
        '''tests the return as dict method in class inventory'''
        sofa_dict = self.sofa.return_as_dictionary()
        assert sofa_dict == {'product_code': 321,
                             'description': 'brown sofa',
                             'market_price': 300,
                             'rental_price': 100,
                             'material': 'Faux Leather',
                             'size': 'Large'}


class ElectricAppliancesTests(TestCase):
    '''tests for the electric appliance module'''
    def setUp(self):
        '''creates a washing machine object'''
        self.washer = ElectricAppliances(2,
                                         'Washing Machine',
                                         500,
                                         200,
                                         'Kenmore',
                                         120)

    def test_init(self):
        '''tests the init for the washer'''
        assert self.washer.product_code == 2
        assert self.washer.description == 'Washing Machine'
        assert self.washer.market_price == 500
        assert self.washer.rental_price == 200
        assert self.washer.brand == 'Kenmore'
        assert self.washer.voltage == 120

    def test_return_as_dict(self):
        '''tests the return as dictionary method'''
        washer_dict = self.washer.return_as_dictionary()
        assert washer_dict == {'product_code': 2,
                               'description': 'Washing Machine',
                               'market_price': 500,
                               'rental_price': 200,
                               'brand': 'Kenmore',
                               'voltage': 120}


class MarketPricesTest(TestCase):
    '''tests the Market Prices Module'''
    def test_get_latest_price(self):
        '''tests that this function will return 24'''
        assert 24 == market_prices.get_latest_price(123)
        assert 24 == market_prices.get_latest_price(74)
