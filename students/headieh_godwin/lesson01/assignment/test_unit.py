"""Unit tests for all classes in the inventory management system"""

import sys
import io
sys.path.append('inventory_management')
from unittest import TestCase
from unittest.mock import patch, MagicMock
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.market_prices as market_prices
from inventory_management import main

# test electrical applicances class
class TestElectricAppliancesClass(TestCase):
    def test_electrical_appliances(self):
        a = {'product_code': '100',
                      'description': 'lamp',
                      'market_price': 40.0,
                      'rental_price': 10.0,
                      'brand': 'Decor Therapy',
                      'voltage': 120}
        d = ('100', 'lamp', 40.0, 10.0, 'Decor Therapy', 120)
        test = ElectricAppliances(*d)
        self.assertEqual(a, test.return_as_dictionary())

# test the furniture class
class TestFurniture(TestCase):
     def test_furniture(self):
        f = {'product_code': '200',
                'description': 'beanbag',
                'market_price': 600.0,
                'rental_price': 100.0,
                'material': 'faux fur',
                'size': 'L'}
        d = ('200', 'beanbag', 600.0, 100.0, 'faux fur', 'L')
        test = Furniture(*d)
        self.assertEqual(f, test.return_as_dictionary())

# test inventory class
class TestInventoryClass(TestCase):
    def test_inventory(self):
        i = {'product_code': '300',
                    'description': 'recliner',
                    'market_price': 60.0,
                    'rental_price': 20.0}
        d = ('300', 'recliner', 60.0, 20.0)
        test = Inventory(*d)
        self.assertEqual(i, test.return_as_dictionary())

# test Market Prices class
class TestMarketPrices(TestCase):
    def test_get_latest_price(self):
        self.assertEqual(24, market_prices.get_latest_price(24))
        self.assertEqual(24, market_prices.get_latest_price(9))

# test main class

item_info = {'product_code': '400',
             'description': "refrigerator",
             'market_price': '800.00',
             'rental_price': '300.00'}
i_obj = ['300', 'recliner', 20.0, 'n', 'n']
f_obj = ['200', 'beanbag', 100.0, 'y', 'faux fur', 'L']
e_obj = ['100', 'lamp', 10.0, 'n', 'y', 'Decor Therapy', 120]

class TestMain(TestCase):

    def test_main_menu(self):
        """Test that input selects the correct menu option"""

        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)

        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)

        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_add_new_items(self):
        Inventory = MagicMock(return_value=0)
        new_item = Inventory(**item_info)
        Inventory.assert_called_with(product_code='400',
                                     description='refrigerator',
                                     market_price='800.00',
                                     rental_price='300.00')

        with patch('market_prices.get_latest_price', return_value=40.0):
            with patch('builtins.input', side_effect=e_obj):
                e_dict = {}
                main.FULLINVENTORY = {}
                main.add_new_item()
                e_dict['100'] = {'product_code': '100',
                                          'description': 'lamp',
                                          'market_price': 40.0,
                                          'rental_price': 10.0,
                                          'brand': 'Decor Therapy',
                                          'voltage': 120}
                self.assertEqual(e_dict, main.FULLINVENTORY)

        with patch('market_prices.get_latest_price', return_value=600.0):
            with patch('builtins.input', side_effect=f_obj):
                f_dict = {}
                main.FULLINVENTORY = {}
                main.add_new_item()
                f_dict['200'] = {'product_code': '200',
                                        'description': 'beanbag',
                                        'market_price': 600.0,
                                        'rental_price': 100.0,
                                        'material': 'faux fur',
                                        'size': 'L'}
                self.assertEqual(f_dict, main.FULLINVENTORY)

        with patch('market_prices.get_latest_price', return_value=60.0):
            with patch('builtins.input', side_effect=i_obj):
                i_dict = {}
                main.FULLINVENTORY = {}
                main.add_new_item()
                i_dict['300'] = {'product_code': '300',
                                         'description': 'recliner',
                                         'market_price': 60.0,
                                         'rental_price': 20.0}
                self.assertEqual(i_dict, main.FULLINVENTORY)

    def test_item_info(self):
        exp_print = ('produce_code: 400\n'
                     'description: refrigerator\n'
                     'market_price: 800.0\n'
                     'rental_price: 300.0\n')

        with patch('builtins.input', side_effect=['400']):
            main.FULLINVENTORY = item_info
            self.assertEqual(main.item_info(), print(exp_print))

        # test if item is not in inventory
        with patch('builtins.input', side_effect=['666']):
            main.FULLINVENTORY = {}
            exp_string = 'Item not found in this inventory'
            self.assertEqual(main.item_info(), print(exp_string))

    def test_get_price(self):
        self.get_price = MagicMock(return_value=24)
        self.assertEqual(main.get_price(5), print('Get price'))

    def test_exit_program(self):
        with self.assertRaises(SystemExit):
            main.exit_program()
