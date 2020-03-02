'''Tests the inventory_management modules'''

import sys
sys.path.append('inventory_management')

from unittest import TestCase
from unittest.mock import patch, MagicMock
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances
import inventory_management.main as main
import inventory_management.market_prices as market_prices

# pylint: disable = C0413

class InventoryClassTest(TestCase):
    '''Tests the inventory_class module'''

    def test_init(self):
        '''Tests the _init_ function'''

        product = Inventory(product_code='M8421',
                            description='Thingabob',
                            market_price=25.99,
                            rental_price=4.99)

        self.assertEqual('M8421', product.product_code)
        self.assertEqual('Thingabob', product.description)
        self.assertEqual(25.99, product.market_price)
        self.assertEqual(4.99, product.rental_price)

    def test_return_as_dictionary(self):
        '''Tests the return_as_dictionary function'''

        product = Inventory(product_code='M8421',
                            description='Thingabob',
                            market_price=25.99,
                            rental_price=4.99)

        test_dict = {}
        test_dict['product_code'] = 'M8421'
        test_dict['description'] = 'Thingabob'
        test_dict['market_price'] = 25.99
        test_dict['rental_price'] = 4.99

        self.assertDictEqual(test_dict, product.return_as_dictionary())


class FurnitureClassTest(TestCase):
    '''Tests the furniture_class module'''

    def test_init(self):
        '''Tests the _init_ function'''

        product = Furniture(product_code='M8421',
                            description='Thingabob',
                            market_price=25.99,
                            rental_price=4.99,
                            material='wood',
                            size='X-Large')

        self.assertEqual('M8421', product.product_code)
        self.assertEqual('Thingabob', product.description)
        self.assertEqual(25.99, product.market_price)
        self.assertEqual(4.99, product.rental_price)

    def test_return_as_dictionary(self):
        '''Tests the return_as_dictionary function'''

        product = Furniture(product_code='M8421',
                            description='Thingabob',
                            market_price=25.99,
                            rental_price=4.99,
                            material='wood',
                            size='X-Large')

        test_dict = {}
        test_dict['product_code'] = 'M8421'
        test_dict['description'] = 'Thingabob'
        test_dict['market_price'] = 25.99
        test_dict['rental_price'] = 4.99
        test_dict['material'] = 'wood'
        test_dict['size'] = 'X-Large'

        self.assertDictEqual(test_dict, product.return_as_dictionary())


class ElectricAppliancesClassTest(TestCase):
    '''Tests the electric_appliances_class module'''

    def test_init(self):
        '''Tests the _init_ function'''

        product = ElectricAppliances(product_code='M8421',
                                     description='Thingabob',
                                     market_price=25.99,
                                     rental_price=4.99,
                                     brand='Acme',
                                     voltage=110)

        self.assertEqual('M8421', product.product_code)
        self.assertEqual('Thingabob', product.description)
        self.assertEqual(25.99, product.market_price)
        self.assertEqual(4.99, product.rental_price)

    def test_return_as_dictionary(self):
        '''Tests the return_as_dictionary function'''

        product = ElectricAppliances(product_code='M8421',
                                     description='Thingabob',
                                     market_price=25.99,
                                     rental_price=4.99,
                                     brand='Acme',
                                     voltage=110)

        test_dict = {}
        test_dict['product_code'] = 'M8421'
        test_dict['description'] = 'Thingabob'
        test_dict['market_price'] = 25.99
        test_dict['rental_price'] = 4.99
        test_dict['brand'] = 'Acme'
        test_dict['voltage'] = 110

        self.assertDictEqual(test_dict, product.return_as_dictionary())


class MarketPricesTest(TestCase):
    '''Tests the market_prices_class module'''

    def test_get_latest_price(self):
        '''Tests the get_latest_price function'''

        market_prices.get_latest_price = MagicMock(return_value=2.98)
        self.assertEqual(market_prices.get_latest_price('test'), 2.98)


class MainTest(TestCase):
    '''Tests the main module'''

    def test_main_menu(self):
        '''Tests the main_menu function'''

        # Tests the menu option '1'
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)

        # Tests the menu option '2'
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)

        # Tests the menu option 'q'
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

    def test_get_price(self):
        '''Tests the set_price function'''

        # Tests return value of 24
        self.assertEqual(main.get_price('test'), 24)

    def test_add_new_item(self):
        '''Tests the add_nem_item function'''

        test_dict = {'bs12': {'product_code': 'bs12',
                              'description': 'Bed Sheets',
                              'market_price': 24,
                              'rental_price': 4.99},
                     'ch02': {'product_code': 'ch02',
                              'description': 'chair',
                              'market_price': 24,
                              'rental_price': 5.99,
                              'material': 'wood',
                              'size': 'XL'},
                     'rf03': {'product_code': 'rf03',
                              'description': 'refrigerator',
                              'market_price': 24,
                              'rental_price': 145.99,
                              'brand': 'GE',
                              'voltage': 110}}

        # Tests the add new item function for an inventory item
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['bs12', 'Bed Sheets', 4.99, 'n', 'n']
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY['bs12'], test_dict['bs12'])

        # Tests the add new item function for a furniture item
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['ch02', 'chair', 5.99, 'y', 'wood', 'XL']
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY['ch02'], test_dict['ch02'])

        # Tests the add new item function for an electrical appliance item
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['rf03', 'refrigerator', 145.99, 'n', 'y', 'GE', 110]
            main.add_new_item()
            self.assertEqual(main.FULL_INVENTORY['rf03'], test_dict['rf03'])

    def test_item_info(self):
        '''Tests the item_info function'''

        test_prods = {'I123': {'product_code': 'I123',
                               'description': 'Thingabob',
                               'market_price': 25.99,
                               'rental_price': 4.99},
                      'C234': {'product_code': 'C234',
                               'description': 'chair',
                               'market_price': 599.99,
                               'rental_price': 39.99,
                               'material': 'wood',
                               'size': 'X-Large'},
                      'E345': {'product_code': 'E345',
                               'description': 'refrigerator',
                               'market_price': 1595.99,
                               'rental_price': 145.99,
                               'brand': 'GE',
                               'voltage': 110}}

        main.FULL_INVENTORY = test_prods

        # Tests the item info function for an inventory item
        market_prices.get_latest_price = MagicMock(retun_value=25.99)
        with patch('builtins.input', side_effect=['I123']):
            self.assertEqual(main.item_info(), print(test_prods.get('I123')))
            self.assertEqual(main.FULL_INVENTORY['I123'], test_prods.get('I123'))

        # Tests the item info function for a furniture item
        market_prices.get_latest_price = MagicMock(retun_value=599.99)
        with patch('builtins.input', side_effect=['C234']):
            self.assertEqual(main.item_info(), print(test_prods.get('C234')))
            self.assertEqual(main.FULL_INVENTORY['C234'], test_prods.get('C234'))

        # Tests the item info function for an electrical appliance item
        market_prices.get_latest_price = MagicMock(retun_value=1595.99)
        with patch('builtins.input', side_effect=['E345']):
            self.assertEqual(main.item_info(), print(test_prods.get('E345')))
            self.assertEqual(main.FULL_INVENTORY['E345'], test_prods.get('E345'))

        # Tests the item info for correct return of an item not in the inventory
        with patch('builtins.input', side_effect=['Z789']):
            self.assertEqual(main.item_info(), print('Item not found in inventory'))

    def test_exit_program(self):
        '''Tests the exit_program function'''

        with self.assertRaises(SystemExit):
            main.exit_program()
