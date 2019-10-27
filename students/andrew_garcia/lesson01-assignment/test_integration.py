import inventory_management.main as main

from unittest import TestCase
from unittest.mock import patch


class TestMain(TestCase):
    def test_add_items(self):
        item_details1 = [25, 'Stool', 25, 'y', 'Wood', 'M']
        inventory1 = {25: {'product_code': 25, 'description': 'Stool', 'market_price': 24,
                           'rental_price': 25, 'material': 'Wood', 'size': 'M'}}

        with patch('builtins.input', side_effect=item_details1):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, inventory1)

        item_details2 = [17, 'Lamp', 50, 'n', 'y', 'SmartLamps', 425]
        inventory2 = {25: {'product_code': 25, 'description': 'Stool', 'market_price': 24,
                           'rental_price': 25, 'material': 'Wood', 'size': 'M'},
                      17: {'product_code': 17, 'description': 'Lamp', 'market_price': 24,
                           'rental_price': 50, 'brand': 'SmartLamps', 'voltage': 425}}

        with patch('builtins.input', side_effect=item_details2):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, inventory2)

        item_details3 = [32, 'Shoe', 50, 'n', 'n']
        inventory3 = {25: {'product_code': 25, 'description': 'Stool', 'market_price': 24,
                           'rental_price': 25, 'material': 'Wood', 'size': 'M'},
                      17: {'product_code': 17, 'description': 'Lamp', 'market_price': 24,
                           'rental_price': 50, 'brand': 'SmartLamps', 'voltage': 425},
                      32: {'product_code': 32, 'description': 'Shoe', 'market_price': 24, 'rental_price': 50}}

        with patch('builtins.input', side_effect=item_details3):
            main.add_new_item()
        self.assertEqual(main.FULL_INVENTORY, inventory3)

        item_dict = {'product_code': 32, 'description': 'Shoe', 'market_price': 24, 'rental_price': 50}
        with patch('builtins.input', side_effect='32'):
            self.assertEqual(main.item_info(), print(item_dict))

