#!/usr/bin/env python3

"""
Unit Testing Inventory Management
"""

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

import inventory_management.market_prices as market_prices
import inventory_management.main as main
from inventory_management.inventory_class import Inventory
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture


class TestMain(TestCase):
    """ test main """

    def setUp(self):
        """ setup """
        self.main = main
        self.mp = market_prices
		
		
    def test_main_menu(self):
        """Test that the user inputs"""

        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)
            
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

            
    def test_get_price(self):
        """Test get_price"""

        self.mp.get_latest_price = MagicMock(return_value=50)
        self.assertEqual(main.get_price('test'), 50)

    def test_add_new_item(self):
        """ tests adding new items to the inventory
            inv == itemcode,descr,rentalprice,isFurn,isAppl
            furn == itemcode,descr,rentalprice,isFurn,isAppl,material,size
            appl == itemcode,descr,rentalprice,isFurn,isAppl,brand,voltage
        """
        item_inv = ['1', 'Shirt', '50', 'n', 'n']
        item_furn = ['2', 'Chair', '100', 'y', 'wood', 'L']
        item_appl = ['3', 'Washer', '200', 'n', 'y', 'Maytag', '120']

        with patch('builtins.input', side_effect = item_inv):
            main.add_new_item()
        with patch('builtins.input', side_effect = item_furn):
            main.add_new_item()
        with patch('builtins.input', side_effect = item_appl):
            main.add_new_item()

        test_dict = {'1':{'product_code': '1',
                          'description': 'Shirt',
                          'market_price': 24,
                          'rental_price': '50'},
                     '2':{'product_code': '2',
                          'description': 'Chair',
                          'market_price': 24,
                          'rental_price': '100',
                          'material': 'wood',
                          'size': 'L'},
                     '3':{'product_code': '3',
                          'description': 'Washer',
                          'market_price': 24,
                          'rental_price': '200',
                          'brand': 'Maytag',
                          'voltage': '120'}}
        self.assertEqual(test_dict, main.return_full_inventory())

    def test_item_info(self):
        """ test returned item info """
        item = ['1', 'Chair', '100', 'y', 'wood', 'L' ]
        with patch('builtins.input', side_effect = item):
            main.add_new_item()

        with patch('builtins.input', side_effect = '1'):
            function = main.item_info()
            info = '\n'.join(('product_code:1',
                          'description:Chair',
                          'market_price:50',
                          'rental_price:100',
                          'material:wood',
                          'size:L'))
            self.assertEqual(function, info)
        
        
class TestInventory(TestCase):
    """ tests for inventory """
    def setUp(self):
        """ creates inventory obj """
        self.inventory = Inventory(1, 'some description', 25, 10.50)

    def test_inventory_init(self):
        """ tests init inventory """
        assert self.inventory.product_code == 1
        assert self.inventory.description == 'some description'
        assert self.inventory.market_price == 25
        assert self.inventory.rental_price == 10.50

    def test_return_as_dict(self):
        """ tests the return dict inventory """
        inventory_dict = self.inventory.return_as_dictionary()
        assert inventory_dict == {'product_code': 1,
                                  'description': 'some description',
                                  'market_price': 25,
                                  'rental_price': 10.50}

                                  
class TestElectricAppliances(TestCase):
    """ test ElectricAppliances """
    def test_electric_appliances(self):
        """Test that an electric appliance object is created"""

        appl = {'product_code': '2',
                    'description': 'Washer',
                    'market_price': 450.0,
                    'rental_price': 125.0,
                    'brand': 'MayTag',
                    'voltage': 110.0}
        item = ('2', 'Washer', 450.0, 125.0, 'MayTag', 110.0)
        item_returned = ElectricAppliances(*item)
        self.assertEqual(appl, item_returned.return_as_dictionary())


class TestFurniture(TestCase):
    """ test furniture """
    def test_furniture(self):
        """Test that a furniture obj created"""

        furn = {'product_code': '3',
                    'description': 'Dresser',
                    'market_price': 350.0,
                    'rental_price': 25.0,
                    'material': 'Pine',
                    'size': 'M'}
        item = ('3', 'Dresser', 350.0, 25.0, 'Pine', 'M')
        item_returned = Furniture(*item)

        self.assertEqual(furn, item_returned.return_as_dictionary())
        
        
class TestMarketPrices(TestCase):
    """ test market_prices return value """

    def setUp(self):
        """ setup """
        self.main = main
        self.mp = market_prices

    def test_get_latest_price(self):
        """ Test get_latest_price mocked return val """

        self.mp.get_latest_price = MagicMock(return_value=50)
        self.assertEqual(50, self.mp.get_latest_price(50))

