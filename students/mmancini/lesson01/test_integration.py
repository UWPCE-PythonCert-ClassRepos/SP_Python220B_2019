#!/usr/bin/env python3

"""
Integration Test Inventory Management System
"""

from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock, MagicMock

from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.market_prices as market_prices
import inventory_management.main as main


class TestIntegration(TestCase):

    def setUp(self):
        """ Setup test """
        self.main = main
        self.mp = market_prices

    def test_integration(self):
        """ test main menu """
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
        """ tests add new items to inventory
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

        """ Test get_price """
        self.assertEqual(main.get_price('test'), 24)
        
        """ test get inventory item info """
        with patch('builtins.input', side_effect = '2'):
            function = main.item_info()
            info = '\n'.join(('product_code:2',
                          'description:Chair',
                          'market_price:24',
                          'rental_price:100',
                          'material:wood',
                          'size:L'))
            self.assertEqual(function, info)

        """ tests item info function when item code is not in the inventory """
        with patch('builtins.input', side_effect = '999'):
            function = main.item_info()
        self.assertEqual(function, 'Item not found in inventory')    

        """ tests exit program """
        with self.assertRaises(SystemExit):
            main.exit_program()

    def test_combo(self):
            self.mp.get_latest_price = MagicMock(return_value=50)
            self.assertEqual(main.get_price('test'), 50)






