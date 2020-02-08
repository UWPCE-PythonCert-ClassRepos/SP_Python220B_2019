#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import patch
import inventory_management.main as main


class TestIntegration(TestCase):
    def test_main(self):
        main.FULL_INVENTORY = {}

        test_furniture = ['BigOlCouch', 'Big, old.', 13, 'Y', 'wood', 'XXL']
        test_electric = ['ABC', 'Meh', 0.99, 'N', 'Y', 'VGood', '220']
        test_inventory = ['BiggerOlCouch', 'Bigger, old.', 99.99, 'N', 'N']

        inventory_dict = {
            'test_furniture': {'productCode': 'BigOlCouch', 'description': 'Big, old.', 'marketPrice': 24,
                               'rentalPrice': 13, 'material': 'wood', 'size': 'XXL'},
            'test_electric': {'productCode': 'ABC', 'description': 'Meh', 'marketPrice': 24, 'rentalPrice': 0.99,
                              'brand': 'VGood', 'voltage': '220'},
            'test_inventory': {'productCode': 'BiggerOlCouch', 'description': 'Bigger, old.', 'marketPrice': 24,
                               'rentalPrice': 99.99}}

        with patch('builtins.input', side_effect=test_furniture):
            main.add_new_item()
        with patch('builtins.input', side_effect=test_electric):
            main.add_new_item()
        with patch('builtins.input', side_effect=test_inventory):
            main.add_new_item()

        self.assertEqual(main.FULL_INVENTORY['BigOlCouch'], inventory_dict['test_furniture'])
        self.assertEqual(main.FULL_INVENTORY['ABC'], inventory_dict['test_electric'])
        self.assertEqual(main.FULL_INVENTORY['BiggerOlCouch'], inventory_dict['test_inventory'])

    def test_info(self):
        main.FULL_INVENTORY = {"BigOlCouch": {"productCode": "BigOlCouch", "description": "Big, old.",
                                              "marketPrice": 24, "rentalPrice": 99.99, "material": "Wood",
                                              "size": "XXL"}}

        with patch('builtins.input', return_value="BigOlCouch"):
            self.assertEqual(print(main.FULL_INVENTORY), main.item_info())

    def test_exit_program(self):
        with self.assertRaises(SystemExit) as context:
            main.exit_program()
        self.assertEqual(context.exception.code, None)
