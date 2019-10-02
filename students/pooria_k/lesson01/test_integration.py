"""Test_unit.py for integration testing of inventory_management"""

from unittest import TestCase
from unittest.mock import Mock, patch
from inventory_management import main

class IntegrationTesting(TestCase):
    """CLass to define Methods for integration testing"""


    """This is the class for testing adding new item to the inventory"""

    def test_addnew_furniture(self):
        """Defining what we will use as input to the addnew_item()"""
        input_furniture = ('444', 'bed', 150, 'y', 'wood', 'L')
        input_app = ('555', 'laptop', 50, 'n', 'y', 'samsung', 120)
        input_inventory = ('666', 'test', 5, 'n', 'n')
        #defining expected output
        expected_item_dic = {'444': {'description': 'bed',
                                     'market_price': 180.0,
                                     'product_code': '444',
                                     'rental_price': 150,
                                     'material': 'wood',
                                     'size': 'L'},
                             '555': {'description': 'laptop',
                                     'market_price': 120.0,
                                     'product_code': '555',
                                     'rental_price': 50,
                                     'brand': 'samsung',
                                     'voltage': 120},
                             '666': {'description': 'test',
                                     'market_price': 10.0,
                                     'product_code': '666',
                                     'rental_price': 5
                                                    }}


        with patch('builtins.input', side_effect=input_furniture):
            # Creating empty FULL_INVENTORY dictionary
            main.FULL_INVENTORY = {}
            # patching item price
            with patch('inventory_management.market_prices.get_latest_price', return_value=180.0):
                main.addnew_item()
                self.assertDictEqual(main.FULL_INVENTORY['444'], expected_item_dic['444'] )

        with patch('builtins.input', side_effect=input_app):
            # main.FULL_INVENTORY = {}
            with patch('inventory_management.market_prices.get_latest_price', return_value=120.0):
                main.addnew_item()
                self.assertDictEqual(main.FULL_INVENTORY['555'], expected_item_dic['555'] )

        with patch('builtins.input', side_effect = input_inventory):
            with patch('inventory_management.market_prices.get_latest_price', return_value=10.0):
                main.addnew_item()
                self.assertEqual(main.FULL_INVENTORY['666'], expected_item_dic['666'])
                self.assertDictEqual(main.FULL_INVENTORY, expected_item_dic)


