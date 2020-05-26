import sys
from unittest import TestCase
from unittest.mock import patch
sys.path.append('./inventory_management')
import main

class integration_test(TestCase):
    def test_addfurn(self):
        input_furniture = ('123', 'bench', 150, 'y', 'wood', 'L')
        expected_item_dic = {'123': {'description': 'bench',
                                     'market_price': 24, # mkt price is static
                                     'item_code': '123',
                                     'rental_price': 150,
                                     'material': 'wood',
                                     'size': 'L'}}
        with patch('builtins.input', side_effect=input_furniture):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            self.assertDictEqual(main.FULL_INVENTORY['123'], expected_item_dic['123'])

    def test_addapp(self):
        input_app = ('456', 'foot masseuse', 50, 'n', 'y', 'Costco', 120)
        expected_item_dic = {'456': {'description': 'foot masseuse',
                                     'market_price': 24,# mkt price is static
                                     'item_code': '456',
                                     'rental_price': 50,
                                     'brand': 'Costco',
                                     'voltage': 120}}
        with patch('builtins.input', side_effect=input_app):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            self.assertDictEqual(main.FULL_INVENTORY['456'], expected_item_dic['456'])

    def test_addinv(self):
        input_inventory = ('789', 'test', 5, 'n', 'n')
        expected_item_dic = {'789': {'description': 'test',
                                     'market_price': 24, # mkt price is static
                                     'item_code': '789',
                                     'rental_price': 5}}
        with patch('builtins.input', side_effect=input_inventory):
            main.FULL_INVENTORY = {}
            main.add_new_item()
            self.assertDictEqual(main.FULL_INVENTORY['789'], expected_item_dic['789'])
