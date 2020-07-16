"""runs Inventory Management tests as a whole"""

import sys
sys.path.append('inventory_management')
from unittest import TestCase, mock
from unittest.mock import patch, MagicMock
from inventory_management.electric_appliances_class import ElectricAppliances
from inventory_management.furniture_class import Furniture
from inventory_management.inventory_class import Inventory
import inventory_management.market_prices as market_prices
from inventory_management import main

#info
item_info = {'product_code': '400',
            'description': "refrigerator",
            'market_price': '800.00',
            'rental_price': '300.00'}
i_obj = ['300', 'recliner', 20.0, 'n', 'n']
f_obj = ['200', 'beanbag', 100.0, 'y', 'faux fur', 'L']
e_obj = ['100', 'lamp', 10.0, 'n', 'y', 'Decor Therapy', 120]

#all are set to 24 dollars since the return value isn't overriden
expected = {
'300': {'product_code': '300', 'description': 'recliner',
        'market_price': 24, 'rental_price': 20.0},
'200': {'product_code': '200', 'description': 'beanbag', 'market_price': 24,
        'rental_price': 100.0, 'material': 'faux fur', 'size': 'L'},
'100': {'product_code': '100', 'description': 'lamp', 'market_price': 24,
        'rental_price': 10.0, 'brand': 'Decor Therapy', 'voltage': 120}
        }

class TestInventoryManagement(TestCase):

    def test_integration(self):
        main.FULLINVENTORY = {}

        #test menu
        with patch('builtins.input', side_effect='1'):
            self.assertEqual(main.main_menu(), main.add_new_item)
        with patch('builtins.input', side_effect='2'):
            self.assertEqual(main.main_menu(), main.item_info)
        with patch('builtins.input', side_effect='q'):
            self.assertEqual(main.main_menu(), main.exit_program)

        #test add item
        with patch('builtins.input', side_effect=i_obj):
            main.add_new_item()
        with patch('builtins.input', side_effect=f_obj):
            main.add_new_item()
        with patch('builtins.input', side_effect=e_obj):
            main.add_new_item()
        self.assertEqual(main.FULLINVENTORY, expected)

#reset fullinventory to just 400 product
        main.FULLINVENTORY = {'400': item_info}
        self.assertEqual(24, main.get_price(400))

# appliance item was added
        with mock.patch("builtins.print") as print_mock, mock.patch("builtins.input") as input_mock:
            input_mock.return_value = "400"

            main.item_info()
            for k, val in item_info.items():
                print_mock.assert_any_call(f"{k}:{val}")
# item info for non existing product
        with mock.patch("builtins.print") as print_mock, mock.patch("builtins.input") as input_mock:
            input_mock.return_value = "666"
            main.item_info()
            print_mock.assert_called_with("Item not found in inventory")
#quit
        with self.assertRaises(SystemExit):
            main.exit_program()
