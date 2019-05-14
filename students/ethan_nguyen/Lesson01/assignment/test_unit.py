from unittest import TestCase
#from unittest.mock import MagicMock
from unittest.mock import patch
import io

from inventory_management.main import main_menu,  get_price, add_new_item
from inventory_management.main import item_info, exit_program, FULL_INVENTORY
from inventory_management.market_prices import get_latest_price
from inventory_management.inventory_class import Inventory
from inventory_management.furniture_class import Furniture
from inventory_management.electric_appliances_class import ElectricAppliances


class InventoryTests(TestCase):

    def test_is_inventory(self):
        snow_board = Inventory('K2', 'Snowboard', 1000, 10)
        self.assertIsInstance(snow_board, Inventory)

    def test_inventory(self):

        gold = {'productCode': 'K2', 'description': 'Snowboard', 
                'marketPrice': 1000, 'rentalPrice': 10}
        snow_board = Inventory('K2', 'Snowboard', 1000, 10)
        self.assertDictEqual(gold, snow_board.return_as_dictionary())


class FurnitureTests(TestCase):

    def test_is_furniture(self):
        chair = Furniture('C1', 'Lounge Chair', 1000, 30, 'Brass', 'Medium')
        self.assertIsInstance(chair, Furniture)

    def test_furniture(self):

        gold = {'productCode': 'C1', 'description': 'Lounge Chair', 
                'marketPrice': 1000, 'rentalPrice': 30, 
                'material': 'Brass', 'size': 'Medium'}

        chair = Furniture('C1', 'Lounge Chair', 1000, 30, 'Brass', 'Medium')

        self.assertDictEqual(gold, chair.return_as_dictionary())


class ElectricApplianceTests(TestCase):

    def test_is_appliance(self):
        tv = ElectricAppliances('OL1', 'OLED TV', 2000, 200, 'LG', 110)
        self.assertIsInstance(tv, ElectricAppliances)

    def test_electric_appliance(self):

        gold = {'productCode': 'OL1', 'description': 'OLED TV', 
                'marketPrice': 2000, 'rentalPrice': 200, 
                'brand': 'LG', 'voltage': 110}

        tv = ElectricAppliances('OL1', 'OLED TV', 2000, 200, 'LG', 110)

        self.assertDictEqual(gold, tv.return_as_dictionary())


class MainUITest(TestCase):

    def test_main_menu(self):

        user_input = ['1', '2', 'q']
        expected_response = ['add_new_item', 'item_info', 'exit_program']

        for iput, res in zip(user_input, expected_response):
            with patch('builtins.input', side_effect=iput):
                response = main_menu()
                self.assertEqual(response.__name__, res)

    def test_get_price(self):
        price = get_price("CL") 
        self.assertEqual(price, 24)

    def test_exit_main(self):
        with self.assertRaises(SystemExit):
            exit_program()

    def test_add_new_item(self):

        #input_inventory = ('K2', 'Snowboard', 1000, 10)
        input_list = [('OL1', 'OLED TV', 2000, 'n', 'y', 'LG', 110), 
                      ('C1', 'Lounge Chair', 1000, 'y', 'Brass', 'L'),
                      ('K2', 'Snowboard', 1000, 'n', 'n')
                      ]
        code_list = ['OL1', 'C1', 'K2']
        gold_list = [{'productCode': 'OL1', 'description': 'OLED TV',
                    'marketPrice': 24, 'rentalPrice': 2000, 'brand': 'LG',
                    'voltage': 110},
                    {'productCode': 'C1', 'description': 'Lounge Chair',
                    'marketPrice': 24, 'rentalPrice': 1000, 
                    'material': 'Brass', 'size': 'L'},
                    {'productCode': 'K2', 'description': 'Snowboard',
                    'marketPrice': 24, 'rentalPrice': 1000}
        ]

        for code, item, gold in zip(code_list, input_list, gold_list):
            with patch('builtins.input', side_effect=item):
                add_new_item()
                self.assertDictEqual(gold, FULL_INVENTORY[code])

    def test_item_info_not_found(self):
        with patch('builtins.input', side_effect="dummy"):
            with patch('sys.stdout', new=io.StringIO()) as actual_result:
                item_info()
        self.assertEqual(actual_result.getvalue(), "Item not found in inventory\n")

    def test_item_info(self):

        input_list = [('OL1', 'OLED TV', 2000, 'n', 'y', 'LG', 110), 
                      ('C1', 'Lounge Chair', 1000, 'y', 'Brass', 'L'),
                      ('K2', 'Snowboard', 1000, 'n', 'n')
                      ]
        gold_list = ['''productCode:OL1
description:OLED TV
marketPrice:24
rentalPrice:2000
brand:LG
voltage:110
''',
'''productCode:C1
description:Lounge Chair
marketPrice:24
rentalPrice:1000
material:Brass
size:L
''',
'''productCode:K2
description:Snowboard
marketPrice:24
rentalPrice:1000
'''
        ]

        for item, print_out in zip(input_list, gold_list):
            with patch('builtins.input', side_effect=item):
                add_new_item()
                with patch('builtins.input', side_effect=item):
                    with patch('sys.stdout', new=io.StringIO()) as actual_result:
                        item_info()
            self.assertEqual(actual_result.getvalue(), print_out)
